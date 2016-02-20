// Generated by gencpp from file rosmod/SetLoggerLevelRequest.msg
// DO NOT EDIT!


#ifndef ROSMOD_MESSAGE_SETLOGGERLEVELREQUEST_H
#define ROSMOD_MESSAGE_SETLOGGERLEVELREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace rosmod
{
template <class ContainerAllocator>
struct SetLoggerLevelRequest_
{
  typedef SetLoggerLevelRequest_<ContainerAllocator> Type;

  SetLoggerLevelRequest_()
    : logger()
    , level()  {
    }
  SetLoggerLevelRequest_(const ContainerAllocator& _alloc)
    : logger(_alloc)
    , level(_alloc)  {
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _logger_type;
  _logger_type logger;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _level_type;
  _level_type level;




  typedef boost::shared_ptr< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> const> ConstPtr;

}; // struct SetLoggerLevelRequest_

typedef ::rosmod::SetLoggerLevelRequest_<std::allocator<void> > SetLoggerLevelRequest;

typedef boost::shared_ptr< ::rosmod::SetLoggerLevelRequest > SetLoggerLevelRequestPtr;
typedef boost::shared_ptr< ::rosmod::SetLoggerLevelRequest const> SetLoggerLevelRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace rosmod

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'rosmod': ['/home/jeb/Repositories/rosmod/comm/src/rosmod/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "51da076440d78ca1684d36c868df61ea";
  }

  static const char* value(const ::rosmod::SetLoggerLevelRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x51da076440d78ca1ULL;
  static const uint64_t static_value2 = 0x684d36c868df61eaULL;
};

template<class ContainerAllocator>
struct DataType< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "rosmod/SetLoggerLevelRequest";
  }

  static const char* value(const ::rosmod::SetLoggerLevelRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string logger\n\
string level\n\
";
  }

  static const char* value(const ::rosmod::SetLoggerLevelRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.logger);
      stream.next(m.level);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct SetLoggerLevelRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::rosmod::SetLoggerLevelRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::rosmod::SetLoggerLevelRequest_<ContainerAllocator>& v)
  {
    s << indent << "logger: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.logger);
    s << indent << "level: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.level);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ROSMOD_MESSAGE_SETLOGGERLEVELREQUEST_H