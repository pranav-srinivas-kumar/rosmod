﻿#ifndef COMPONENT_HPP
#define COMPONENT_HPP

#include <iostream>
#include <string>
#include <std_msgs/Bool.h>
#include "node/xmlParser.hpp"
#include "node/Logger.hpp"

#ifdef USE_ROSMOD
  #include "rosmod/rosmod_ros.h"
  #include "rosmod/rosmod_callback_queue.h"
#else
  #ifdef USE_ROSCPP
    #include "ros/ros.h"
    #include "ros/callback_queue.h"
  #endif
#endif

class Component {
public:
  // Constructor
  Component(ComponentConfig &_config, int argc, char **argv);

  // Start up
  virtual void startUp() = 0;

  // Initialization
  virtual void Init(const NAMESPACE::TimerEvent& event);

  // Synchronization
  virtual void component_synchronization_OnOneData(const std_msgs::Bool::ConstPtr& received_data);

  // Callback Queue Handler
  void processQueue();

  // Destructor
  ~Component();

protected:
  ComponentConfig config;
  int node_argc;
  char **node_argv;
  NAMESPACE::Publisher comp_sync_pub;
  NAMESPACE::Subscriber comp_sync_sub;
  NAMESPACE::Timer initOneShotTimer;
  NAMESPACE::CallbackQueue compQueue;
  std::unique_ptr<Logger> logger;
};

#endif
