﻿#ifndef COMPONENT_HPP
#define COMPONENT_HPP

#include "ros/ros.h"

#include "cluster_flight_application/xmlParser.hpp"

// required for the callback queue
#include <ros/callback_queue.h>

class Component
{
    public:
        // Component Constructor
        Component(std::string hostName, std::string nodeName, std::string compName, int argc, char **argv);

	// StartUp will be completely generated
	virtual void startUp() = 0;

	// Init will be generated with BL supplied by user
	virtual void Init(const ros::TimerEvent& event);

	// queueThread processes queue actions
	void processQueue();

	// required for clean shutdown
	~Component();

    protected:
        std::string hostName;
        std::string nodeName;
        std::string compName;
        int node_argc;
        char **node_argv;
	ros::Timer initOneShotTimer;  // timer for calling init
	ros::CallbackQueue compQueue; // single callbackQueue for the component
};

#endif
