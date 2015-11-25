// Generated by gencpp from file client_server_package/Power.msg
// DO NOT EDIT!


#ifndef CLIENT_SERVER_PACKAGE_MESSAGE_POWER_H
#define CLIENT_SERVER_PACKAGE_MESSAGE_POWER_H

#include <ros/service_traits.h>


#include <client_server_package/PowerRequest.h>
#include <client_server_package/PowerResponse.h>


namespace client_server_package
{

struct Power
{

typedef PowerRequest Request;
typedef PowerResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct Power
} // namespace client_server_package


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::client_server_package::Power > {
  static const char* value()
  {
    return "5b953294a1eff28068639768c321cf6d";
  }

  static const char* value(const ::client_server_package::Power&) { return value(); }
};

template<>
struct DataType< ::client_server_package::Power > {
  static const char* value()
  {
    return "client_server_package/Power";
  }

  static const char* value(const ::client_server_package::Power&) { return value(); }
};


// service_traits::MD5Sum< ::client_server_package::PowerRequest> should match 
// service_traits::MD5Sum< ::client_server_package::Power > 
template<>
struct MD5Sum< ::client_server_package::PowerRequest>
{
  static const char* value()
  {
    return MD5Sum< ::client_server_package::Power >::value();
  }
  static const char* value(const ::client_server_package::PowerRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::client_server_package::PowerRequest> should match 
// service_traits::DataType< ::client_server_package::Power > 
template<>
struct DataType< ::client_server_package::PowerRequest>
{
  static const char* value()
  {
    return DataType< ::client_server_package::Power >::value();
  }
  static const char* value(const ::client_server_package::PowerRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::client_server_package::PowerResponse> should match 
// service_traits::MD5Sum< ::client_server_package::Power > 
template<>
struct MD5Sum< ::client_server_package::PowerResponse>
{
  static const char* value()
  {
    return MD5Sum< ::client_server_package::Power >::value();
  }
  static const char* value(const ::client_server_package::PowerResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::client_server_package::PowerResponse> should match 
// service_traits::DataType< ::client_server_package::Power > 
template<>
struct DataType< ::client_server_package::PowerResponse>
{
  static const char* value()
  {
    return DataType< ::client_server_package::Power >::value();
  }
  static const char* value(const ::client_server_package::PowerResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // CLIENT_SERVER_PACKAGE_MESSAGE_POWER_H
