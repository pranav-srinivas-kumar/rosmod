#include "agse_package/radial_actuator_controller.hpp"

//# Start User Globals Marker
#include <stdlib.h>
//# End User Globals Marker

// Initialization Function
//# Start Init Marker
void radial_actuator_controller::init_timer_operation(const NAMESPACE::TimerEvent& event)
{
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Entering radial_actuator_controller::init_timer_operation");
#endif
  // Initialize Here
  paused = true;
  lowerLimitReached = false;

  // THESE NEED TO BE UPDATED
  epsilon = 100;
  motorForwardPin = 87; //88;     // connected to GPIO2_24, pin P8_28
  motorBackwardPin = 86; //89;    // connected to GPIO2_25, pin P8_30
  lowerLimitSwitchPin = 27;       // connected to GPIO0_27, pin P8_17
  
  adcPin = 0;  // connected to ADC0, pin P9_39

  // set up the pins to control the h-bridge
  gpio_export(motorForwardPin);
  gpio_export(motorBackwardPin);
  gpio_export(lowerLimitSwitchPin);
  gpio_set_dir(motorForwardPin,OUTPUT_PIN);
  gpio_set_dir(motorBackwardPin,OUTPUT_PIN);
  gpio_set_dir(lowerLimitSwitchPin,INPUT_PIN);
  // set up the encoder module
  rm_eqep_period = 1000000000L;
  radialMotoreQEP.initialize("/sys/devices/ocp.3/48304000.epwmss/48304180.eqep", eQEP::eQEP_Mode_Absolute);
  radialMotoreQEP.set_period(rm_eqep_period);

  // Command line args for radial goal
  for (int i = 0; i < node_argc; i++)
    {
      if (!strcmp(node_argv[i], "-unpaused"))
	{
	  paused = false;
	}
      if (!strcmp(node_argv[i], "-r"))
	{
	  radialGoal = atoi(node_argv[i+1]);
	}
      if (!strcmp(node_argv[i], "-e"))
	{
	  epsilon = atoi(node_argv[i+1]);
	}
    }

  ROS_INFO("RADIAL GOAL SET TO : %d",radialGoal);

  // Stop Init Timer
  init_timer.stop();
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Exiting radial_actuator_controller::init_timer_operation");
#endif  
}
//# End Init Marker



// Subscriber Operation - controlInputs_sub
//# Start controlInputs_sub_operation Marker
void radial_actuator_controller::controlInputs_sub_operation(const agse_package::controlInputs::ConstPtr& received_data)
{
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Entering radial_actuator_controller::controlInputs_sub_operation");
#endif
  // Business Logic for controlInputs_sub_operation
  paused = received_data->paused;
  
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Exiting radial_actuator_controller::controlInputs_sub_operation");
#endif
}
//# End controlInputs_sub_operation Marker

// Server Operation - radialPos_server
//# Start radialPos_operation Marker
bool radial_actuator_controller::radialPos_operation(agse_package::radialPos::Request  &req,
  agse_package::radialPos::Response &res)
{
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Entering radial_actuator_controller::radialPos_operation");
#endif
  // Business Logic for radialPos_server_operation
    if (req.update == true)
    {
      //      ROS_INFO("GOT NEW RADIAL GOAL: %d",(int)req.goal);
      //      ROS_INFO("CURRENT RADIUS: %d",radialCurrent);
      radialGoal = req.goal;
    }
  if (req.setZeroPosition == true)
    {
      ROS_INFO("ZEROED RADIAL ENCODER");
      radialMotoreQEP.set_position(0);
    }
  res.lowerLimitReached = lowerLimitReached;
  res.upperLimitReached = false;
  res.current = radialCurrent;
  return true;

#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Exiting radial_actuator_controller::radialPos_operation");
#endif
  return true;
}
//# End radialPos_operation Marker

// Timer Callback - radialPosTimer
//# Start radialPosTimer_operation Marker
void radial_actuator_controller::radialPosTimer_operation(const NAMESPACE::TimerEvent& event)
{
#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Entering radial_actuator_controller::radialPosTimer_operation");
#endif
  // Business Logic for radialPosTimer_operation
  if (!paused)
    {
      // read current value for radial position (encoder)
      radialCurrent = radialMotoreQEP.get_position();
      //ROS_INFO("Raidal Actuator Encoder Reading: %d",radialCurrent);

      unsigned int limitSwitchState = 0;
      unsigned int backwardPinState = 0;
      gpio_get_value(lowerLimitSwitchPin,&limitSwitchState);
      gpio_get_value(motorBackwardPin,&backwardPinState);
      if (backwardPinState && !limitSwitchState)
	{
	  lowerLimitReached = true;
	}
      // update motor based on current value
      if ( abs(radialGoal-radialCurrent) > epsilon ) // if there's significant reason to move
	{
	  if (radialGoal > radialCurrent) 
	    {
	      lowerLimitReached = false;
	      gpio_set_value(motorBackwardPin,LOW);
	      gpio_set_value(motorForwardPin,HIGH);
	    }
	  else
	    {
	      gpio_set_value(motorForwardPin,LOW);
	      gpio_set_value(motorBackwardPin,HIGH);
	    }
	}
      else
	{
	  gpio_set_value(motorForwardPin,LOW);
	  gpio_set_value(motorBackwardPin,LOW);
	}
    }
  else 
    {
      gpio_set_value(motorForwardPin,LOW);
      gpio_set_value(motorBackwardPin,LOW);      
    }

#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->log("DEBUG", "Exiting radial_actuator_controller::radialPosTimer_operation");
#endif
}
//# End radialPosTimer_operation Marker


// Destructor - Cleanup Ports & Timers
radial_actuator_controller::~radial_actuator_controller()
{
  radialPosTimer.stop();
  controlInputs_sub.shutdown();
  radialPos_server.shutdown();
  //# Start Destructor Marker
  //# End Destructor Marker
}

// Startup - Setup Component Ports & Timers
void radial_actuator_controller::startUp()
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

  logger->create_file("/var/log/" + config.nodeName + "." + config.compName + ".log");
  logger->set_is_periodic(config.is_periodic_logging);
  logger->set_max_log_unit(config.periodic_log_unit);

#ifdef USE_ROSMOD
  comp_queue.ROSMOD_LOGGER->create_file("/var/log/ROSMOD_DEBUG." + config.nodeName + "." + config.compName + ".log");
  comp_queue.ROSMOD_LOGGER->set_is_periodic(config.is_periodic_logging);
  comp_queue.ROSMOD_LOGGER->set_max_log_unit(config.periodic_log_unit);
#endif    
  
#ifdef USE_ROSMOD 
  this->comp_queue.scheduling_scheme = config.schedulingScheme;
  rosmod::ROSMOD_Callback_Options callback_options;
#endif  
  // Configure all provided services associated with this component
#ifdef USE_ROSMOD  
  callback_options.alias = "radialPos_operation";
  callback_options.priority = 50;
  callback_options.deadline.sec =0;
  callback_options.deadline.nsec = 100000000;
#endif    
  // Component Server - radialPos_server
  advertiseName = "radialPos";
  if (config.portGroupMap.find("radialPos_server") != config.portGroupMap.end())
    advertiseName += "_" + config.portGroupMap["radialPos_server"];
  NAMESPACE::AdvertiseServiceOptions radialPos_server_server_options;
  radialPos_server_server_options = NAMESPACE::AdvertiseServiceOptions::create<agse_package::radialPos>
      (advertiseName.c_str(),
       boost::bind(&radial_actuator_controller::radialPos_operation, this, _1, _2),
       NAMESPACE::VoidPtr(),
#ifdef USE_ROSMOD       
       &this->comp_queue,
       callback_options);
#else
       &this->comp_queue);
#endif
  this->radialPos_server = nh.advertiseService(radialPos_server_server_options);

  if (config.num_comps_to_sync > 1 )
    {
      // Synchronize components now that all publishers and servers have been initialized
      this->comp_sync_pub = nh.advertise<std_msgs::Bool>("component_synchronization", 1000);
  
#ifdef USE_ROSMOD  
      rosmod::SubscribeOptions comp_sync_sub_options;
      rosmod::ROSMOD_Callback_Options sync_callback_options;
#else
      ros::SubscribeOptions comp_sync_sub_options;
#endif
      ros::Duration(config.comp_sync_timeout/2.0).sleep();
      comp_sync_sub_options = NAMESPACE::SubscribeOptions::create<std_msgs::Bool>
	("component_synchronization",
	 1000,
	 boost::bind(&radial_actuator_controller::component_sync_operation, this, _1),
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
      ros::Duration(config.comp_sync_timeout/2.0).sleep();
      this->comp_sync_sub.shutdown();  
      this->comp_sync_pub.shutdown();
    }

  // Configure all subscribers associated with this component
#ifdef USE_ROSMOD 
  callback_options.alias = "controlInputs_sub_operation";
  callback_options.priority = 50;
  callback_options.deadline.sec = 0;
  callback_options.deadline.nsec = 100000000;
#endif  
  // Component Subscriber - controlInputs_sub
  advertiseName = "controlInputs";
  if (config.portGroupMap.find("controlInputs_sub") != config.portGroupMap.end())
    advertiseName += "_" + config.portGroupMap["controlInputs_sub"];
  NAMESPACE::SubscribeOptions controlInputs_sub_options;
  controlInputs_sub_options = NAMESPACE::SubscribeOptions::create<agse_package::controlInputs>
      (advertiseName.c_str(),
       1000,
       boost::bind(&radial_actuator_controller::controlInputs_sub_operation, this, _1),
       NAMESPACE::VoidPtr(),
#ifdef USE_ROSMOD
       &this->comp_queue,
       callback_options);
#else
       &this->comp_queue);
#endif 
  controlInputs_sub_options.transport_hints = NAMESPACE::TransportHints().udp();
  this->controlInputs_sub = nh.subscribe(controlInputs_sub_options);

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
     boost::bind(&radial_actuator_controller::init_timer_operation, this, _1),
     &this->comp_queue,
#ifdef USE_ROSMOD     
     callback_options,
#endif     
     true,
     false); 
  this->init_timer = nh.createTimer(timer_options);
  this->init_timer.stop();
#ifdef USE_ROSMOD   
  callback_options.alias = "radialPosTimer_operation";
  callback_options.priority = 50;
  callback_options.deadline.sec = 0;
  callback_options.deadline.nsec = 100000000;
#endif
  // Component Timer - radialPosTimer
  timer_options = 
    NAMESPACE::TimerOptions
    (ros::Duration(0.01),
     boost::bind(&radial_actuator_controller::radialPosTimer_operation, this, _1),
     &this->comp_queue,
#ifdef USE_ROSMOD     
     callback_options,
#endif 
     false,
     false);
  this->radialPosTimer = nh.createTimer(timer_options);


  this->init_timer.start();
  this->radialPosTimer.start();
}

extern "C" {
  Component *maker(ComponentConfig &config, int argc, char **argv) {
    return new radial_actuator_controller(config,argc,argv);
  }
}
