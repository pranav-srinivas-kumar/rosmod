#include <sstream>
#include <fcntl.h>
#include <cerrno>
#include <cstring>
#include <typeinfo>

#include "ros/common.h"
#include "ros/io.h"
#include "rosmod/subscription.h"
#include "rosmod/publication.h"
#include "rosmod/transport_publisher_link.h"
#include "rosmod/intraprocess_publisher_link.h"
#include "rosmod/intraprocess_subscriber_link.h"
#include "ros/connection.h"
#include "ros/transport/transport_tcp.h"
#include "ros/transport/transport_udp.h"
#include "ros/callback_queue_interface.h"
#include "rosmod/cmq.h"
#include "ros/this_node.h"
#include "ros/network.h"
#include "ros/poll_manager.h"
#include "ros/connection_manager.h"
#include "ros/message_deserializer.h"
#include "ros/subscription_queue.h"
#include "ros/file_log.h"
#include "ros/transport_hints.h"
#include "ros/subscription_callback_helper.h"

#include <boost/make_shared.hpp>

using XmlRpc::XmlRpcValue;

namespace ros
{

Subscription2::Subscription2(const std::string &name, const std::string& md5sum, const std::string& datatype, const TransportHints& transport_hints)
: name_(name)
, md5sum_(md5sum)
, datatype_(datatype)
, nonconst_callbacks_(0)
, dropped_(false)
, shutting_down_(false)
, transport_hints_(transport_hints)
{
}

Subscription2::~Subscription2()
{
  pending_connections_.clear();
  callbacks_.clear();
}

void Subscription2::shutdown()
{
  {
    boost::mutex::scoped_lock lock(shutdown_mutex_);
    shutting_down_ = true;
  }

  drop();
}

XmlRpcValue Subscription2::getStats()
{
  XmlRpcValue stats;
  stats[0] = name_;
  XmlRpcValue conn_data;
  conn_data.setSize(0);

  boost::mutex::scoped_lock lock(publisher_links_mutex_);

  uint32_t cidx = 0;
  for (V_PublisherLink2::iterator c = publisher_links_.begin();
       c != publisher_links_.end(); ++c)
  {
    const PublisherLink2::Stats& s = (*c)->getStats();
    conn_data[cidx][0] = (*c)->getConnectionID();
    conn_data[cidx][1] = (int)s.bytes_received_;
    conn_data[cidx][2] = (int)s.messages_received_;
    conn_data[cidx][3] = (int)s.drops_;
    conn_data[cidx][4] = 0; // figure out something for this. not sure.
  }

  stats[1] = conn_data;
  return stats;
}

// [(connection_id, publisher_xmlrpc_uri, direction, transport, topic_name, connected, connection_info_string)*]
// e.g. [(1, 'http://host:54893/', 'i', 'TCPROS', '/chatter', 1, 'TCPROS connection on port 59746 to [host:34318 on socket 11]')]
void Subscription2::getInfo(XmlRpc::XmlRpcValue& info)
{
  boost::mutex::scoped_lock lock(publisher_links_mutex_);

  for (V_PublisherLink2::iterator c = publisher_links_.begin();
       c != publisher_links_.end(); ++c)
  {
    XmlRpcValue curr_info;
    curr_info[0] = (int)(*c)->getConnectionID();
    curr_info[1] = (*c)->getPublisherXMLRPCURI();
    curr_info[2] = "i";
    curr_info[3] = (*c)->getTransportType();
    curr_info[4] = name_;
    curr_info[5] = true; // For length compatibility with rospy
    curr_info[6] = (*c)->getTransportInfo();
    info[info.size()] = curr_info;
  }
}

uint32_t Subscription2::getNumPublishers()
{
	boost::mutex::scoped_lock lock(publisher_links_mutex_);
	return (uint32_t)publisher_links_.size();
}

void Subscription2::drop()
{
  if (!dropped_)
  {
    dropped_ = true;

    dropAllConnections();
  }
}

void Subscription2::dropAllConnections()
{
  // Swap our subscribers list with a local one so we can only lock for a short period of time, because a
  // side effect of our calling drop() on connections can be re-locking the subscribers mutex
  V_PublisherLink2 localsubscribers;

  {
    boost::mutex::scoped_lock lock(publisher_links_mutex_);

    localsubscribers.swap(publisher_links_);
  }

  V_PublisherLink2::iterator it = localsubscribers.begin();
  V_PublisherLink2::iterator end = localsubscribers.end();
  for (;it != end; ++it)
  {
    (*it)->drop();
  }
}

void Subscription2::addLocalConnection(const PublicationPtr2& pub)
{
  boost::mutex::scoped_lock lock(publisher_links_mutex_);
  if (dropped_)
  {
    return;
  }

  ROSCPP_LOG_DEBUG("Creating intraprocess link for topic [%s]", name_.c_str());

  IntraProcessPublisherLinkPtr2 pub_link(new IntraProcessPublisherLink2(shared_from_this(), XMLRPCManager::instance()->getServerURI(), transport_hints_));
  IntraProcessSubscriberLinkPtr2 sub_link(new IntraProcessSubscriberLink2(pub));
  pub_link->setPublisher(sub_link);
  sub_link->setSubscriber(pub_link);

  addPublisherLink(pub_link);
  pub->addSubscriberLink(sub_link);
}

bool urisEqual(const std::string& uri1, const std::string& uri2)
{
  std::string host1, host2;
  uint32_t port1 = 0, port2 = 0;
  network::splitURI(uri1, host1, port1);
  network::splitURI(uri2, host2, port2);
  return port1 == port2 && host1 == host2;
}

bool Subscription2::pubUpdate(const V_string& new_pubs)
{
  boost::mutex::scoped_lock lock(shutdown_mutex_);

  if (shutting_down_ || dropped_)
  {
    return false;
  }

  bool retval = true;

  {
    std::stringstream ss;

    for (V_string::const_iterator up_i = new_pubs.begin();
         up_i != new_pubs.end(); ++up_i)
    {
      ss << *up_i << ", ";
    }

    ss << " already have these connections: ";
    for (V_PublisherLink2::iterator spc = publisher_links_.begin();
         spc!= publisher_links_.end(); ++spc)
    {
      ss << (*spc)->getPublisherXMLRPCURI() << ", ";
    }

    boost::mutex::scoped_lock lock(pending_connections_mutex_);
    S_PendingConnection::iterator it = pending_connections_.begin();
    S_PendingConnection::iterator end = pending_connections_.end();
    for (; it != end; ++it)
    {
      ss << (*it)->getRemoteURI() << ", ";
    }

    ROSCPP_LOG_DEBUG("Publisher update for [%s]: %s", name_.c_str(), ss.str().c_str());
  }

  V_string additions;
  V_PublisherLink2 subtractions;
  V_PublisherLink2 to_add;
  // could use the STL set operations... but these sets are so small
  // it doesn't really matter.
  {
    boost::mutex::scoped_lock lock(publisher_links_mutex_);

    for (V_PublisherLink2::iterator spc = publisher_links_.begin();
         spc!= publisher_links_.end(); ++spc)
    {
      bool found = false;
      for (V_string::const_iterator up_i = new_pubs.begin();
           !found && up_i != new_pubs.end(); ++up_i)
      {
        if (urisEqual((*spc)->getPublisherXMLRPCURI(), *up_i))
        {
          found = true;
          break;
        }
      }

      if (!found)
      {
        subtractions.push_back(*spc);
      }
    }

    for (V_string::const_iterator up_i  = new_pubs.begin(); up_i != new_pubs.end(); ++up_i)
    {
      bool found = false;
      for (V_PublisherLink2::iterator spc = publisher_links_.begin();
           !found && spc != publisher_links_.end(); ++spc)
      {
        if (urisEqual(*up_i, (*spc)->getPublisherXMLRPCURI()))
        {
          found = true;
          break;
        }
      }

      if (!found)
      {
        boost::mutex::scoped_lock lock(pending_connections_mutex_);
        S_PendingConnection::iterator it = pending_connections_.begin();
        S_PendingConnection::iterator end = pending_connections_.end();
        for (; it != end; ++it)
        {
          if (urisEqual(*up_i, (*it)->getRemoteURI()))
          {
            found = true;
            break;
          }
        }
      }

      if (!found)
      {
        additions.push_back(*up_i);
      }
    }
  }

  for (V_PublisherLink2::iterator i = subtractions.begin(); i != subtractions.end(); ++i)
  {
	const PublisherLinkPtr2& link = *i;
    if (link->getPublisherXMLRPCURI() != XMLRPCManager::instance()->getServerURI())
    {
      ROSCPP_LOG_DEBUG("Disconnecting from publisher [%s] of topic [%s] at [%s]",
                        link->getCallerID().c_str(), name_.c_str(), link->getPublisherXMLRPCURI().c_str());
		  link->drop();
	  }
	  else
	  {
		  ROSCPP_LOG_DEBUG("Disconnect: skipping myself for topic [%s]", name_.c_str());
	  }
	}

  for (V_string::iterator i = additions.begin();
            i != additions.end(); ++i)
  {
    // this function should never negotiate a self-subscription
    if (XMLRPCManager::instance()->getServerURI() != *i)
    {
      retval &= negotiateConnection(*i);
    }
    else
    {
      ROSCPP_LOG_DEBUG("Skipping myself (%s, %s)", name_.c_str(), XMLRPCManager::instance()->getServerURI().c_str());
    }
  }

  return retval;
}

bool Subscription2::negotiateConnection(const std::string& xmlrpc_uri)
{
  XmlRpcValue tcpros_array, protos_array, params;
  XmlRpcValue udpros_array;
  TransportUDPPtr udp_transport;
  int protos = 0;
  V_string transports = transport_hints_.getTransports();
  if (transports.empty())
  {
    transport_hints_.reliable();
    transports = transport_hints_.getTransports();
  }
  for (V_string::const_iterator it = transports.begin();
       it != transports.end();
       ++it)
  {
    if (*it == "UDP")
    {
      int max_datagram_size = transport_hints_.getMaxDatagramSize();
      udp_transport = TransportUDPPtr(new TransportUDP(&PollManager::instance()->getPollSet()));
      if (!max_datagram_size)
        max_datagram_size = udp_transport->getMaxDatagramSize();
      udp_transport->createIncoming(0, false);
      udpros_array[0] = "UDPROS";
      M_string m;
      m["topic"] = getName();
      m["md5sum"] = md5sum();
      m["callerid"] = this_node::getName();
      m["type"] = datatype();
      boost::shared_array<uint8_t> buffer;
      uint32_t len;
      Header::write(m, buffer, len);
      XmlRpcValue v(buffer.get(), len);
      udpros_array[1] = v;
      udpros_array[2] = network::getHost();
      udpros_array[3] = udp_transport->getServerPort();
      udpros_array[4] = max_datagram_size;

      protos_array[protos++] = udpros_array;
    }
    else if (*it == "TCP")
    {
      tcpros_array[0] = std::string("TCPROS");
      protos_array[protos++] = tcpros_array;
    }
    else
    {
      ROS_WARN("Unsupported transport type hinted: %s, skipping", it->c_str());
    }
  }
  params[0] = this_node::getName();
  params[1] = name_;
  params[2] = protos_array;
  std::string peer_host;
  uint32_t peer_port;
  if (!network::splitURI(xmlrpc_uri, peer_host, peer_port))
  {
    ROS_ERROR("Bad xml-rpc URI: [%s]", xmlrpc_uri.c_str());
    return false;
  }

  XmlRpc::XmlRpcClient* c = new XmlRpc::XmlRpcClient(peer_host.c_str(),
                                                     peer_port, "/");
 // if (!c.execute("requestTopic", params, result) || !g_node->validateXmlrpcResponse("requestTopic", result, proto))

  // Initiate the negotiation.  We'll come back and check on it later.
  if (!c->executeNonBlock("requestTopic", params))
  {
    ROSCPP_LOG_DEBUG("Failed to contact publisher [%s:%d] for topic [%s]",
              peer_host.c_str(), peer_port, name_.c_str());
    delete c;
    if (udp_transport)
    {
      udp_transport->close();
    }

    return false;
  }

  ROSCPP_LOG_DEBUG("Began asynchronous xmlrpc connection to [%s:%d]", peer_host.c_str(), peer_port);

  // The PendingConnectionPtr takes ownership of c, and will delete it on
  // destruction.
  PendingConnectionPtr conn(new PendingConnection(c, udp_transport, shared_from_this(), xmlrpc_uri));

  XMLRPCManager::instance()->addASyncConnection(conn);
  // Put this connection on the list that we'll look at later.
  {
    boost::mutex::scoped_lock pending_connections_lock(pending_connections_mutex_);
    pending_connections_.insert(conn);
  }

  return true;
}

void closeTransport(const TransportUDPPtr& trans)
{
  if (trans)
  {
    trans->close();
  }
}

void Subscription2::pendingConnectionDone(const PendingConnectionPtr& conn, XmlRpcValue& result)
{
  boost::mutex::scoped_lock lock(shutdown_mutex_);
  if (shutting_down_ || dropped_)
  {
    return;
  }

  {
    boost::mutex::scoped_lock pending_connections_lock(pending_connections_mutex_);
    pending_connections_.erase(conn);
  }

  TransportUDPPtr udp_transport;

  std::string peer_host = conn->getClient()->getHost();
  uint32_t peer_port = conn->getClient()->getPort();
  std::stringstream ss;
  ss << "http://" << peer_host << ":" << peer_port << "/";
  std::string xmlrpc_uri = ss.str();
  udp_transport = conn->getUDPTransport();

  XmlRpc::XmlRpcValue proto;
  if(!XMLRPCManager::instance()->validateXmlrpcResponse("requestTopic", result, proto))
  {
  	ROSCPP_LOG_DEBUG("Failed to contact publisher [%s:%d] for topic [%s]",
              peer_host.c_str(), peer_port, name_.c_str());
  	closeTransport(udp_transport);
  	return;
  }

  if (proto.size() == 0)
  {
  	ROSCPP_LOG_DEBUG("Couldn't agree on any common protocols with [%s] for topic [%s]", xmlrpc_uri.c_str(), name_.c_str());
  	closeTransport(udp_transport);
  	return;
  }

  if (proto.getType() != XmlRpcValue::TypeArray)
  {
  	ROSCPP_LOG_DEBUG("Available protocol info returned from %s is not a list.", xmlrpc_uri.c_str());
  	closeTransport(udp_transport);
  	return;
  }
  if (proto[0].getType() != XmlRpcValue::TypeString)
  {
  	ROSCPP_LOG_DEBUG("Available protocol info list doesn't have a string as its first element.");
  	closeTransport(udp_transport);
  	return;
  }

  std::string proto_name = proto[0];
  if (proto_name == "TCPROS")
  {
    if (proto.size() != 3 ||
        proto[1].getType() != XmlRpcValue::TypeString ||
        proto[2].getType() != XmlRpcValue::TypeInt)
    {
    	ROSCPP_LOG_DEBUG("publisher implements TCPROS, but the " \
                "parameters aren't string,int");
      return;
    }
    std::string pub_host = proto[1];
    int pub_port = proto[2];
    ROSCPP_LOG_DEBUG("Connecting via tcpros to topic [%s] at host [%s:%d]", name_.c_str(), pub_host.c_str(), pub_port);

    TransportTCPPtr transport(new TransportTCP(&PollManager::instance()->getPollSet()));
    if (transport->connect(pub_host, pub_port))
    {
      ConnectionPtr connection(new Connection());
      TransportPublisherLinkPtr2 pub_link(new TransportPublisherLink2(shared_from_this(), xmlrpc_uri, transport_hints_));

      connection->initialize(transport, false, HeaderReceivedFunc());
      pub_link->initialize(connection);

      ConnectionManager::instance()->addConnection(connection);

      boost::mutex::scoped_lock lock(publisher_links_mutex_);
      addPublisherLink(pub_link);

      ROSCPP_LOG_DEBUG("Connected to publisher of topic [%s] at [%s:%d]", name_.c_str(), pub_host.c_str(), pub_port);
    }
    else
    {
    	ROSCPP_LOG_DEBUG("Failed to connect to publisher of topic [%s] at [%s:%d]", name_.c_str(), pub_host.c_str(), pub_port);
    }
  }
  else if (proto_name == "UDPROS")
  {
    if (proto.size() != 6 ||
        proto[1].getType() != XmlRpcValue::TypeString ||
        proto[2].getType() != XmlRpcValue::TypeInt ||
        proto[3].getType() != XmlRpcValue::TypeInt ||
        proto[4].getType() != XmlRpcValue::TypeInt ||
        proto[5].getType() != XmlRpcValue::TypeBase64)
    {
      ROSCPP_LOG_DEBUG("publisher implements UDPROS, but the " \
	    	       "parameters aren't string,int,int,int,base64");
      closeTransport(udp_transport);
      return;
    }
    std::string pub_host = proto[1];
    int pub_port = proto[2];
    int conn_id = proto[3];
    int max_datagram_size = proto[4];
    std::vector<char> header_bytes = proto[5];
    boost::shared_array<uint8_t> buffer = boost::shared_array<uint8_t>(new uint8_t[header_bytes.size()]);
    memcpy(buffer.get(), &header_bytes[0], header_bytes.size());
    Header h;
    std::string err;
    if (!h.parse(buffer, header_bytes.size(), err))
    {
      ROSCPP_LOG_DEBUG("Unable to parse UDPROS connection header: %s", err.c_str());
      closeTransport(udp_transport);
      return;
    }
    ROSCPP_LOG_DEBUG("Connecting via udpros to topic [%s] at host [%s:%d] connection id [%08x] max_datagram_size [%d]", name_.c_str(), pub_host.c_str(), pub_port, conn_id, max_datagram_size);

    std::string error_msg;
    if (h.getValue("error", error_msg))
    {
      ROSCPP_LOG_DEBUG("Received error message in header for connection to [%s]: [%s]", xmlrpc_uri.c_str(), error_msg.c_str());
      closeTransport(udp_transport);
      return;
    }

    TransportPublisherLinkPtr2 pub_link(new TransportPublisherLink2(shared_from_this(), xmlrpc_uri, transport_hints_));
    if (pub_link->setHeader(h))
    {
      ConnectionPtr connection(new Connection());
      connection->initialize(udp_transport, false, NULL);
      connection->setHeader(h);
      pub_link->initialize(connection);

      ConnectionManager::instance()->addConnection(connection);

      boost::mutex::scoped_lock lock(publisher_links_mutex_);
      addPublisherLink(pub_link);

      ROSCPP_LOG_DEBUG("Connected to publisher of topic [%s] at [%s:%d]", name_.c_str(), pub_host.c_str(), pub_port);
    }
    else
    {
      ROSCPP_LOG_DEBUG("Failed to connect to publisher of topic [%s] at [%s:%d]", name_.c_str(), pub_host.c_str(), pub_port);
      closeTransport(udp_transport);
      return;
    }
  }
  else
  {
  	ROSCPP_LOG_DEBUG("Publisher offered unsupported transport [%s]", proto_name.c_str());
  }
}

uint32_t Subscription2::handleMessage(const SerializedMessage& m, bool ser, bool nocopy, const boost::shared_ptr<M_string>& connection_header, const PublisherLinkPtr2& link)
{
  boost::mutex::scoped_lock lock(callbacks_mutex_);

  uint32_t drops = 0;

  // Cache the deserializers by type info.  If all the subscriptions are the same type this has the same performance as before.  If
  // there are subscriptions with different C++ type (but same ROS message type), this now works correctly rather than passing
  // garbage to the messages with different C++ types than the first one.
  cached_deserializers_.clear();

  ros::Time receipt_time = ros::Time::now();

  for (V_CallbackInfo::iterator cb = callbacks_.begin();
       cb != callbacks_.end(); ++cb)
  {
    const CallbackInfoPtr& info = *cb;

    ROS_ASSERT(info->callback_queue_);

    const std::type_info* ti = &info->helper_->getTypeInfo();

    if ((nocopy && m.type_info && *ti == *m.type_info) || (ser && (!m.type_info || *ti != *m.type_info)))
    {
      MessageDeserializerPtr deserializer;

      V_TypeAndDeserializer::iterator des_it = cached_deserializers_.begin();
      V_TypeAndDeserializer::iterator des_end = cached_deserializers_.end();
      for (; des_it != des_end; ++des_it)
      {
        if (*des_it->first == *ti)
        {
          deserializer = des_it->second;
          break;
        }
      }

      if (!deserializer)
      {
        deserializer = boost::make_shared<MessageDeserializer>(info->helper_, m, connection_header);
        cached_deserializers_.push_back(std::make_pair(ti, deserializer));
      }

      bool was_full = false;
      bool nonconst_need_copy = false;
      if (callbacks_.size() > 1)
      {
        nonconst_need_copy = true;
      }

      info->subscription_queue_->push(info->helper_, deserializer, info->has_tracked_object_, info->tracked_object_, nonconst_need_copy, receipt_time, &was_full);

      if (was_full)
      {
        ++drops;
      }
      else
      {
        info->callback_queue_->addCallback(info->subscription_queue_, info->priority, (uint64_t)info.get());
      }
    }
  }

  // measure statistics
  statistics_.callback(connection_header, name_, link->getCallerID(), m, link->getStats().bytes_received_, receipt_time, drops > 0);

  // If this link is latched, store off the message so we can immediately pass it to new subscribers later
  if (link->isLatched())
  {
    LatchInfo li;
    li.connection_header = connection_header;
    li.link = link;
    li.message = m;
    li.receipt_time = receipt_time;
    latched_messages_[link] = li;
  }

  cached_deserializers_.clear();

  return drops;
}

bool Subscription2::addCallback(const SubscriptionCallbackHelperPtr& helper, const std::string& md5sum, CMQ* queue, int priority, int32_t queue_size, const VoidConstPtr& tracked_object, bool allow_concurrent_callbacks)
{
  ROS_ASSERT(helper);
  ROS_ASSERT(queue);

  statistics_.init(helper);

  // Decay to a real type as soon as we have a subscriber with a real type
  {
    boost::mutex::scoped_lock lock(md5sum_mutex_);
    if (md5sum_ == "*" && md5sum != "*")
    {

      md5sum_ = md5sum;
    }
  }

  if (md5sum != "*" && md5sum != this->md5sum())
  {
    return false;
  }

  {
    boost::mutex::scoped_lock lock(callbacks_mutex_);

    CallbackInfoPtr info(new CallbackInfo);
    info->helper_ = helper;
    info->callback_queue_ = queue;
    info->priority = priority;
    this->priority_ = priority;
    info->subscription_queue_.reset(new SubscriptionQueue(name_, queue_size, allow_concurrent_callbacks));
    info->tracked_object_ = tracked_object;
    info->has_tracked_object_ = false;
    if (tracked_object)
    {
      info->has_tracked_object_ = true;
    }

    if (!helper->isConst())
    {
      ++nonconst_callbacks_;
    }

    callbacks_.push_back(info);
    cached_deserializers_.reserve(callbacks_.size());

    // if we have any latched links, we need to immediately schedule callbacks
    if (!latched_messages_.empty())
    {
      boost::mutex::scoped_lock lock(publisher_links_mutex_);

      V_PublisherLink2::iterator it = publisher_links_.begin();
      V_PublisherLink2::iterator end = publisher_links_.end();
      for (; it != end;++it)
      {
        const PublisherLinkPtr2& link = *it;
        if (link->isLatched())
        {
          M_PublisherLinkToLatchInfo::iterator des_it = latched_messages_.find(link);
          if (des_it != latched_messages_.end())
          {
            const LatchInfo& latch_info = des_it->second;

            MessageDeserializerPtr des(new MessageDeserializer(helper, latch_info.message, latch_info.connection_header));
            bool was_full = false;
            info->subscription_queue_->push(info->helper_, des, info->has_tracked_object_, info->tracked_object_, true, latch_info.receipt_time, &was_full);
            if (!was_full)
            {
              info->callback_queue_->addCallback(info->subscription_queue_, info->priority, (uint64_t)info.get());
            }
          }
        }
      }
    }
  }

  return true;
}

void Subscription2::removeCallback(const SubscriptionCallbackHelperPtr& helper)
{
  CallbackInfoPtr info;
  {
    boost::mutex::scoped_lock cbs_lock(callbacks_mutex_);
    for (V_CallbackInfo::iterator it = callbacks_.begin();
         it != callbacks_.end(); ++it)
    {
      if ((*it)->helper_ == helper)
      {
        info = *it;
        callbacks_.erase(it);

        if (!helper->isConst())
        {
          --nonconst_callbacks_;
        }

        break;
      }
    }
  }

  if (info)
  {
    info->subscription_queue_->clear();
    info->callback_queue_->removeByID((uint64_t)info.get());
  }
}

void Subscription2::headerReceived(const PublisherLinkPtr2& link, const Header& h)
{
  boost::mutex::scoped_lock lock(md5sum_mutex_);
  if (md5sum_ == "*")
  {
    md5sum_ = link->getMD5Sum();
  }
}

void Subscription2::addPublisherLink(const PublisherLinkPtr2& link)
{
  publisher_links_.push_back(link);
}

void Subscription2::removePublisherLink(const PublisherLinkPtr2& pub_link)
{
  boost::mutex::scoped_lock lock(publisher_links_mutex_);

  V_PublisherLink2::iterator it = std::find(publisher_links_.begin(), publisher_links_.end(), pub_link);
  if (it != publisher_links_.end())
  {
    publisher_links_.erase(it);
  }

  if (pub_link->isLatched())
  {
    latched_messages_.erase(pub_link);
  }
}

void Subscription2::getPublishTypes(bool& ser, bool& nocopy, const std::type_info& ti)
{
  boost::mutex::scoped_lock lock(callbacks_mutex_);
  for (V_CallbackInfo::iterator cb = callbacks_.begin();
       cb != callbacks_.end(); ++cb)
  {
    const CallbackInfoPtr& info = *cb;
    if (info->helper_->getTypeInfo() == ti)
    {
      nocopy = true;
    }
    else
    {
      ser = true;
    }

    if (nocopy && ser)
    {
      return;
    }
  }
}

const std::string Subscription2::datatype()
{
  return datatype_;
}

const std::string Subscription2::md5sum()
{
  boost::mutex::scoped_lock lock(md5sum_mutex_);
  return md5sum_;
}

}
