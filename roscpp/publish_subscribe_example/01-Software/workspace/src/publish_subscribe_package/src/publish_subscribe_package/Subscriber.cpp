#include "publish_subscribe_package/Subscriber.hpp"

//# Start User Globals Marker
//# End User Globals Marker

// Initialization Function
//# Start Init Marker
void Subscriber::Init(const ros::TimerEvent& event)
{
  // Initialize Here

  // Stop Init Timer
  initOneShotTimer.stop();
}
//# End Init Marker

// Subscriber Callback - subscriber_port
//# Start subscriber_port_OnOneData Marker
void Subscriber::subscriber_port_OnOneData(const publish_subscribe_package::Message::ConstPtr& received_data)
{
  // Business Logic for subscriber_port Subscriber
  LOGGER.INFO("Subscriber::Subscriber_Port::Received Message - %s", received_data->name.c_str());
}
//# End subscriber_port_OnOneData Marker


// Destructor - Cleanup Ports & Timers
Subscriber::~Subscriber()
{
  subscriber_port.shutdown();
  //# Start Destructor Marker
  //# End Destructor Marker
}

// Startup - Setup Component Ports & Timers
void Subscriber::startUp()
{
  ros::NodeHandle nh;
  std::string advertiseName;

  // Component Subscriber - subscriber_port
  advertiseName = "Message";
  if (portGroupMap.find("subscriber_port") != portGroupMap.end())
    advertiseName += "_" + portGroupMap["subscriber_port"];
  ros::SubscribeOptions subscriber_port_options;
  subscriber_port_options = ros::SubscribeOptions::create<publish_subscribe_package::Message>
      (advertiseName.c_str(),
       1000,
       boost::bind(&Subscriber::subscriber_port_OnOneData, this, _1),
       ros::VoidPtr(),
       &this->compQueue);
  this->subscriber_port = nh.subscribe(subscriber_port_options);

  // Init Timer
  ros::TimerOptions timer_options;
  timer_options = 
    ros::TimerOptions
    (ros::Duration(-1),
     boost::bind(&Subscriber::Init, this, _1),
     &this->compQueue,
     true);
  this->initOneShotTimer = nh.createTimer(timer_options);  
  
  // Identify the pwd of Node Executable
  std::string s = node_argv[0];
  std::string exec_path = s;
  std::string delimiter = "/";
  std::string exec, pwd;
  size_t pos = 0;
  while ((pos = s.find(delimiter)) != std::string::npos) {
    exec = s.substr(0, pos);
    s.erase(0, pos + delimiter.length());
  }
  exec = s.substr(0, pos);
  pwd = exec_path.erase(exec_path.find(exec), exec.length());
  std::string log_file_path = pwd + nodeName + "." + compName + ".log"; 
  
  // Create the log file & open file stream
  LOGGER.CREATE_FILE(log_file_path);
  
  // Establish log levels of LOGGER
  LOGGER.SET_LOG_LEVELS(logLevels);
}

extern "C" {
  Component *maker(ComponentConfig &config, int argc, char **argv) {
    return new Subscriber(config,argc,argv);
  }
}
