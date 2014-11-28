#include "ros/ros.h"
#include "wam_application/LRImageVector.h"

#include <sstream>

std::string nodeName;

int main(int argc, char **argv)
{
  if ( argc != 2)
    {
      ROS_INFO("usage: LowResolution_a <satellite name>");
      return 1;
    }
  nodeName = argv[1];
  ros::init(argc, argv, "LowResolution_a");

  ros::NodeHandle n;

  ros::Publisher lrImage_pub = n.advertise<wam_application::LRImageVector>("LRImageVector", 1000);

  ros::Rate loop_rate(10);

  while (ros::ok())
    {
      wam_application::LRImageVector lowResImgVec;

      lowResImgVec.img[0] = 400;

      lrImage_pub.publish(lowResImgVec);

      ROS_INFO("Published Low Resolution Image from satellite %s", nodeName.c_str());

      ros::spinOnce();

      loop_rate.sleep();
    }


  return 0;
}
