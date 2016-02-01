#ifndef CLIENT_HPP
#define CLIENT_HPP
#include "node/Component.hpp"
#include "client_server_package/Power.h"

#ifdef USE_ROSMOD
  #include "rosmod/rosmod_ros.h"
#else
  #ifdef USE_ROSCPP
    #include "ros/ros.h"
  #endif
#endif



//# Start User Includes Marker
//# End User Includes Marker

//# Start User Globals Marker
//# End User Globals Marker

class Client : public Component
{
public:
  // Constructor
  Client(ComponentConfig& _config, int argc, char **argv)
  : Component(_config, argc, argv) {}

  // Initialization
  void init_timer_operation(const NAMESPACE::TimerEvent& event);

  // Timer Operation - client_timer
  void client_timer_operation(const NAMESPACE::TimerEvent& event);

  // Start up
  void startUp();

  // Destructor
  ~Client();

private:

  // Timer
  NAMESPACE::Timer client_timer;

  // Client 
  NAMESPACE::ServiceClient client_port;

  //# Start User Private Variables Marker
  //# End User Private Variables Marker
};

#endif
