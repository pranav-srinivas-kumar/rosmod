#include "client_server_package/Client.hpp"

//# Start User Globals Marker
#include <stdlib.h>
#include <boost/random/linear_congruential.hpp>
#include <boost/random/uniform_int.hpp>
#include <boost/random/uniform_real.hpp>
#include <boost/random/variate_generator.hpp>
#include <boost/generator_iterator.hpp>
#include <boost/random/mersenne_twister.hpp>
//# End User Globals Marker

// Initialization Function
//# Start Init Marker
void Client::init_timer_operation(const NAMESPACE::TimerEvent& event)
{
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Entering Client::init_timer_operation");
#endif
  // Initialize Here
  // Stop Init Timer
  init_timer.stop();
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Exiting Client::init_timer_operation");
#endif  
}
//# End Init Marker


// Timer Callback - client_timer
//# Start client_timer_operation Marker
#pragma optimize( "", off )
void Client::client_timer_operation(const NAMESPACE::TimerEvent& event)
{
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Entering Client::client_timer_operation");
#endif

  boost::random::mt19937 rng;
  boost::random::uniform_int_distribution<> loop_iteration_random(2520000, 4200000);
  int loop_max = loop_iteration_random(rng);
  
  // Business Logic for client_timer_operation
  for(int i=0; i < loop_max; i++) {
    double result = 0.0;
    double x = 41865185131.214415;
    double y = 562056205.1515;
    result = x*y;
  }  
  client_server_package::Power power_function;
  power_function.request.base = float(rand() % 10);
  power_function.request.exponent = float(rand() % 10);
  logger->log("INFO", "Client::Client Timer::Sending Request to calculate %f ^ %f", 
	      power_function.request.base, 
	      power_function.request.exponent);
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "BEFORE CLIENT CALL");
#endif  
  if (client_port.call(power_function))
    logger->log("INFO", 
		"Client::Client Timer::Server Response - %f", power_function.response.result);
  else {
    logger->log("ERROR", "Client::Client Timer::Failed to invoke Server Operation");
    client_port.waitForExistence(ros::Duration(-1));
  }
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "CLIENT CALL COMPLETED");
#endif  
  
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Exiting Client::client_timer_operation");
#endif
}
#pragma optimize( "", on )
//# End client_timer_operation Marker


// Destructor - Cleanup Ports & Timers
Client::~Client()
{
  client_timer.stop();
  client_port.shutdown();
  //# Start Destructor Marker
  //# End Destructor Marker
}

// Startup - Setup Component Ports & Timers
void Client::startUp()
{
  NAMESPACE::NodeHandle nh;
  std::string advertiseName;

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
  std::string log_file_path = pwd + config.nodeName + "." + config.compName + ".log"; 

  logger->create_file(pwd + config.nodeName + "." + config.compName + ".log");
  logger->set_is_periodic(config.is_periodic_logging);
  logger->set_max_log_unit(config.periodic_log_unit);

#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->create_file(pwd + "ROSMOD_DEBUG." + config.nodeName + "." + config.compName + ".log");
  comp_queue.ROSMOD_LOGGER->set_is_periodic(config.is_periodic_logging);
  comp_queue.ROSMOD_LOGGER->set_max_log_unit(config.periodic_log_unit);
#endif    
  
#ifdef USE_ROSMOD 
  this->comp_queue.scheduling_scheme = config.schedulingScheme;
  rosmod::ROSMOD_Callback_Options callback_options;
#endif  

  // Synchronize components now that all publishers and servers have been initialized
  this->comp_sync_pub = nh.advertise<std_msgs::Bool>("component_synchronization", 1000);
  
#ifdef USE_ROSMOD  
  rosmod::SubscribeOptions comp_sync_sub_options;
  rosmod::ROSMOD_Callback_Options sync_callback_options;
#else
  ros::SubscribeOptions comp_sync_sub_options;
#endif
  
  comp_sync_sub_options = NAMESPACE::SubscribeOptions::create<std_msgs::Bool>
    ("component_synchronization",
     1000,
     boost::bind(&Client::component_sync_operation, this, _1),
     NAMESPACE::VoidPtr(),
#ifdef USE_ROSMOD     
     &this->comp_queue,
     sync_callback_options);
#else
     &this->comp_queue);
#endif
  this->comp_sync_sub = nh.subscribe(comp_sync_sub_options);

  ros::Time now = ros::Time::now();
  while ( this->comp_sync_sub.getNumPublishers() < this->config.num_comps_to_sync &&
	  (ros::Time::now() - now) < ros::Duration(config.comp_sync_timeout))
  ros::Duration(0.1).sleep();
  ros::Duration(0.5).sleep();
  this->comp_sync_sub.shutdown();  
  this->comp_sync_pub.shutdown();


  // Configure all required services associated with this component
  // Component Client - client_port
  advertiseName = "Power";
  if (config.portGroupMap.find("client_port") != config.portGroupMap.end())
    advertiseName += "_" + config.portGroupMap["client_port"];
  this->client_port = nh.serviceClient<client_server_package::Power>(advertiseName.c_str(), true); 

  // Init Timer
#ifdef USE_ROSMOD    
  callback_options.alias = "init_timer_operation";
  callback_options.priority = 99;
  callback_options.deadline.sec = 1;
  callback_options.deadline.nsec = 0;
#endif
  NAMESPACE::TimerOptions timer_options;
  timer_options = 
    NAMESPACE::TimerOptions
    (ros::Duration(-1),
     boost::bind(&Client::init_timer_operation, this, _1),
     &this->comp_queue,
#ifdef USE_ROSMOD     
     callback_options,
#endif     
     true,
     false); 
  this->init_timer = nh.createTimer(timer_options);
  this->init_timer.stop();
#ifdef USE_ROSMOD   
  callback_options.alias = "client_timer_operation";
  callback_options.priority = 50;
  callback_options.deadline.sec = 3;
  callback_options.deadline.nsec = 0;
#endif
  // Component Timer - client_timer
  timer_options = 
    NAMESPACE::TimerOptions
    (ros::Duration(5.0),
     boost::bind(&Client::client_timer_operation, this, _1),
     &this->comp_queue,
#ifdef USE_ROSMOD     
     callback_options,
#endif 
     false,
     false);
  this->client_timer = nh.createTimer(timer_options);


  this->init_timer.start();
  this->client_timer.start();
}

extern "C" {
  Component *maker(ComponentConfig &config, int argc, char **argv) {
    return new Client(config,argc,argv);
  }
}
