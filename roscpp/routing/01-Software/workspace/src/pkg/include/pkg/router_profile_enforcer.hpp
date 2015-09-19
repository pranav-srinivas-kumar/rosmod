#ifndef ROUTER_PROFILE_ENFORCER_HPP
#define ROUTER_PROFILE_ENFORCER_HPP
#include "ros/ros.h"
#include "node/Component.hpp"



//# Start User Includes Marker
//# End User Includes Marker

//# Start User Globals Marker
//# End User Globals Marker

class router_profile_enforcer : public Component
{
public:
  // Constructor
  router_profile_enforcer(ComponentConfig& _config, int argc, char **argv) : Component(_config, argc, argv) {}

  // Initialization
  void Init(const ros::TimerEvent& event);

  // Start up
  void startUp();

  // Destructor
  ~router_profile_enforcer();

private:

  //# Start User Private Variables Marker
  //# End User Private Variables Marker
};

#endif
