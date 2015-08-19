#ifndef NETWORK_RECEIVER_HPP
#define NETWORK_RECEIVER_HPP

#include "ros/ros.h"

#include <arpa/inet.h>
#include <boost/thread/thread.hpp>

#include "network/NetworkProfile.hpp"
#include "network/buffer.hpp"
#include <std_msgs/UInt64MultiArray.h>

namespace Network
{
  static const std::string oob_mc_group = "224.0.0.251";
  static const int oob_mc_port = 12345;
  
  class receiver
  {
  public:
    receiver();

    int init(std::string profileName, uint64_t buffer_capacity_bits);
    void add_sender(std::string profileName);

    void set_duration(double dur) { duration = ros::Duration(dur); }
    void set_output_filename(std::string filename) { output_filename = filename; }

    void update_sender_stream(uint64_t uuid, ros::Time t, uint64_t new_size);

    ros::Time get_end_time() const { return ros::Time(endTime); }

    int oob_send(std::vector<uint64_t>& send_uuids, bool val);

    void buffer_receive_thread(void);

    int unlimit_ddos(void);
    int limit_ddos(ros::Time now, double timeWindow);

  public:
    message_buffer<Network::Message> buffer;
    Network::NetworkProfile profile;
    
  private:
    std::vector<Network::Message> messages;
    ros::Duration duration;
    ros::Time endTime;
    bool received_data;

    struct sockaddr_in oob_mc_send_sockaddr;
    int oob_mc_send_sockfd;

    std::string output_filename;

    std::vector<uint64_t> uuids;
    std::vector<uint64_t> disabled_uuids;
    std::map<uint64_t, Network::NetworkProfile> profile_map;
    std::map<uint64_t, std::map<ros::Time, uint64_t>> receive_map; // uuid - > <time, data>
  };
};

#endif
