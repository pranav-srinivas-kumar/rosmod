#include "ros/ros.h"
#include "satellite_flight_application/SatState.h"
#include "satellite_flight_application/SatelliteState.h"
#include "satellite_flight_application/ThrusterComm.h"
#include "satellite_flight_application/TargetOrbit.h"
#include <cstdlib>

ros::ServiceClient thrusterControlClient;
std::string nodeName;

void targetOrbitCallback(const satellite_flight_application::TargetOrbit::ConstPtr& orbit)
{
  ROS_INFO("I got a new target orbit!");
  ROS_INFO("Activating satellite %s thrusters to achieve new orbit", nodeName.c_str());

  satellite_flight_application::ThrusterComm srv;
  if (thrusterControlClient.call(srv))
    {
      ROS_INFO("Successfully activated satellite thrusters");
    }
  else
    {
      ROS_ERROR("Failed to activate satellite thrusters");
      thrusterControlClient.waitForExistence(ros::Duration(-1));
    }
}

int main(int argc, char **argv)
{
  if ( argc != 2)
    {
      ROS_INFO("usage: OrbitController_a <satellite name>");
      return 1;
    }
  std::string actorName = "OrbitController_a";
  actorName += argv[1];
  nodeName = argv[1];

  ros::init(argc, argv, actorName.c_str());

  ros::NodeHandle n;

  std::string stateServiceName = "SatelliteState";
  stateServiceName += argv[1];

  ros::ServiceClient satStateClient = n.serviceClient<satellite_flight_application::SatelliteState>(stateServiceName.c_str());

  std::string thrusterServiceName = "ThrusterComm";
  thrusterServiceName += argv[1];

  thrusterControlClient = n.serviceClient<satellite_flight_application::ThrusterComm>(thrusterServiceName.c_str());

  ros::Publisher satStatePub = n.advertise<satellite_flight_application::SatState>("SatState", 1000);

  ros::Subscriber targetOrbitSub = n.subscribe("TargetOrbit", 1000, targetOrbitCallback);

  satStateClient.waitForExistence(ros::Duration(-1));
  thrusterControlClient.waitForExistence(ros::Duration(-1));
  
  ros::Rate loop_rate(1);

  while (ros::ok())
    {
      satellite_flight_application::SatelliteState srv;
      if (satStateClient.call(srv))
	{
	  ROS_INFO("Got state vector from satellite %s bus", nodeName.c_str());
	}
      else
	{
	  ROS_ERROR("Failed to get satellite state vector for satellite %s.", nodeName.c_str());
	  satStateClient.waitForExistence(ros::Duration(-1));
	}

      satellite_flight_application::SatState satState;
      satState.sat_id = nodeName;
      satStatePub.publish(satState);

      ros::spinOnce();

      loop_rate.sleep();
    }

  return 0;
}
