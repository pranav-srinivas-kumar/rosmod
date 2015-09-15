#include "dsc/sumo_intf.hpp"

SUMO_CLIENT sumo_client;

//# Start User Globals Marker
//# End User Globals Marker

// Initialization Function
//# Start Init Marker
void sumo_intf::Init(const ros::TimerEvent& event)
{
  // Initialize Here
  std::string sumo_host;
  int sumo_port;
  for (int i=0; i<node_argc; i++)
    {
      if (!strcmp(node_argv[i], "--sumo_host"))
	{
	  sumo_host = node_argv[i+1];
	}
      if (!strcmp(node_argv[i], "--sumo_port"))
	{
	  sumo_port = atoi(node_argv[i+1]);
	}
    }
  sumo_client.create_connection(sumo_port, sumo_host);
  // Stop Init Timer
  initOneShotTimer.stop();
}
//# End Init Marker


// Server Callback - sumo_il_get_vehicle_number_server
//# Start sumo_il_get_vehicle_numberCallback Marker
bool sumo_intf::sumo_il_get_vehicle_numberCallback(dsc::sumo_il_get_vehicle_number::Request  &req,
  dsc::sumo_il_get_vehicle_number::Response &res)
{
  // Business Logic for sumo_il_get_vehicle_number_server Server
  if ( _il_num_vehicles_map.find( req.sensor_name ) == _il_num_vehicles_map.end() )
    {
      int numVehicles;
      sumo_client.getLastStepInductionLoopVehicleNumber( req.sensor_name, numVehicles );
      _il_num_vehicles_map[ req.sensor_name ] = numVehicles;
    }
  res.num_vehicles = _il_num_vehicles_map[ req.sensor_name ];
  _il_num_vehicles_map[ req.sensor_name ] = 0;
  return true;
}
//# End sumo_il_get_vehicle_numberCallback Marker
// Server Callback - sumo_il_get_vehicle_ids_server
//# Start sumo_il_get_vehicle_idsCallback Marker
bool sumo_intf::sumo_il_get_vehicle_idsCallback(dsc::sumo_il_get_vehicle_ids::Request  &req,
  dsc::sumo_il_get_vehicle_ids::Response &res)
{
  // Business Logic for sumo_il_get_vehicle_ids_server Server
  if ( _il_vehicle_ids_map.find( req.sensor_name ) == _il_vehicle_ids_map.end() )
    {
      std::vector<std::string> ids;
      sumo_client.getLastStepInductionLoopVehicleIDs( req.sensor_name, ids );
      _il_vehicle_ids_map[ req.sensor_name ] = ids;
    }
  res.vehicle_ids = _il_vehicle_ids_map[ req.sensor_name ];
  _il_vehicle_ids_map[ req.sensor_name ] = std::vector<std::string>();
  return true;
}
//# End sumo_il_get_vehicle_idsCallback Marker
// Server Callback - sumo_tlc_get_ryg_state_server
//# Start sumo_tlc_get_ryg_stateCallback Marker
bool sumo_intf::sumo_tlc_get_ryg_stateCallback(dsc::sumo_tlc_get_ryg_state::Request  &req,
  dsc::sumo_tlc_get_ryg_state::Response &res)
{
  // Business Logic for sumo_tlc_get_ryg_state_server Server
  if ( _tl_state_map.find( req.intersection_name ) == _tl_state_map.end() )
    {
      std::string state;
      sumo_client.getRedYellowGreenState( req.intersection_name, state );
      _tl_state_map[ req.intersection_name ] = state;
    }
  res.ryg_state = _tl_state_map[ req.intersection_name ];
  return true;
}
//# End sumo_tlc_get_ryg_stateCallback Marker
// Server Callback - sumo_tlc_set_ryg_state_server
//# Start sumo_tlc_set_ryg_stateCallback Marker
bool sumo_intf::sumo_tlc_set_ryg_stateCallback(dsc::sumo_tlc_set_ryg_state::Request  &req,
  dsc::sumo_tlc_set_ryg_state::Response &res)
{
  // Business Logic for sumo_tlc_set_ryg_state_server Server
  sumo_client.setRedYellowGreenState( req.intersection_name, req.ryg_state );
  return true;
}
//# End sumo_tlc_set_ryg_stateCallback Marker

// Timer Callback - sumo_step_timer
//# Start sumo_step_timerCallback Marker
void sumo_intf::sumo_step_timerCallback(const ros::TimerEvent& event)
{
  // Business Logic for sumo_step_timer Timer
  // STEP THE SIMULATION
  sumo_client.commandSimulationStep(0);
  // UPDATE ALL SENSOR DATA
  for (auto it = _il_num_vehicles_map.begin(); it != _il_num_vehicles_map.end(); ++it)
    {
      int tmp;
      sumo_client.getLastStepInductionLoopVehicleNumber( it->first, tmp );
      it->second += tmp;
    }
  for (auto it = _il_vehicle_ids_map.begin(); it != _il_vehicle_ids_map.end(); ++it)
    {
      std::vector<std::string> tmp;
      sumo_client.getLastStepInductionLoopVehicleIDs( it->first, tmp );
      for (auto tmp_id=tmp.begin(); tmp_id!=tmp.end(); ++tmp_id)
	{
	  if ( std::find(it->second.begin(), it->second.end(), *tmp_id) == it->second.end())
	    {
	      it->second.push_back(*tmp_id);
	    }
	}
    }
  for (auto it = _tl_state_map.begin(); it != _tl_state_map.end(); ++it)
    {
      std::string tmp;
      sumo_client.getRedYellowGreenState( it->first, tmp );
      it->second = tmp;
    }
}
//# End sumo_step_timerCallback Marker


// Destructor - Cleanup Ports & Timers
sumo_intf::~sumo_intf()
{
  sumo_step_timer.stop();
  sumo_il_get_vehicle_number_server.shutdown();
  sumo_il_get_vehicle_ids_server.shutdown();
  sumo_tlc_get_ryg_state_server.shutdown();
  sumo_tlc_set_ryg_state_server.shutdown();
  //# Start Destructor Marker
  //# End Destructor Marker
}

// Startup - Setup Component Ports & Timers
void sumo_intf::startUp()
{
  ros::NodeHandle nh;
  std::string advertiseName;

  // Scheduling Scheme is FIFO

  // Component Server - sumo_il_get_vehicle_number_server
  advertiseName = "sumo_il_get_vehicle_number";
  if (portGroupMap.find("sumo_il_get_vehicle_number_server") != portGroupMap.end())
    advertiseName += "_" + portGroupMap["sumo_il_get_vehicle_number_server"];
  ros::AdvertiseServiceOptions sumo_il_get_vehicle_number_server_server_options;
  sumo_il_get_vehicle_number_server_server_options = ros::AdvertiseServiceOptions::create<dsc::sumo_il_get_vehicle_number>
      (advertiseName.c_str(),
       boost::bind(&sumo_intf::sumo_il_get_vehicle_numberCallback, this, _1, _2),
       ros::VoidPtr(),
       &this->compQueue);
  this->sumo_il_get_vehicle_number_server = nh.advertiseService(sumo_il_get_vehicle_number_server_server_options);  
  // Component Server - sumo_il_get_vehicle_ids_server
  advertiseName = "sumo_il_get_vehicle_ids";
  if (portGroupMap.find("sumo_il_get_vehicle_ids_server") != portGroupMap.end())
    advertiseName += "_" + portGroupMap["sumo_il_get_vehicle_ids_server"];
  ros::AdvertiseServiceOptions sumo_il_get_vehicle_ids_server_server_options;
  sumo_il_get_vehicle_ids_server_server_options = ros::AdvertiseServiceOptions::create<dsc::sumo_il_get_vehicle_ids>
      (advertiseName.c_str(),
       boost::bind(&sumo_intf::sumo_il_get_vehicle_idsCallback, this, _1, _2),
       ros::VoidPtr(),
       &this->compQueue);
  this->sumo_il_get_vehicle_ids_server = nh.advertiseService(sumo_il_get_vehicle_ids_server_server_options);  
  // Component Server - sumo_tlc_get_ryg_state_server
  advertiseName = "sumo_tlc_get_ryg_state";
  if (portGroupMap.find("sumo_tlc_get_ryg_state_server") != portGroupMap.end())
    advertiseName += "_" + portGroupMap["sumo_tlc_get_ryg_state_server"];
  ros::AdvertiseServiceOptions sumo_tlc_get_ryg_state_server_server_options;
  sumo_tlc_get_ryg_state_server_server_options = ros::AdvertiseServiceOptions::create<dsc::sumo_tlc_get_ryg_state>
      (advertiseName.c_str(),
       boost::bind(&sumo_intf::sumo_tlc_get_ryg_stateCallback, this, _1, _2),
       ros::VoidPtr(),
       &this->compQueue);
  this->sumo_tlc_get_ryg_state_server = nh.advertiseService(sumo_tlc_get_ryg_state_server_server_options);  
  // Component Server - sumo_tlc_set_ryg_state_server
  advertiseName = "sumo_tlc_set_ryg_state";
  if (portGroupMap.find("sumo_tlc_set_ryg_state_server") != portGroupMap.end())
    advertiseName += "_" + portGroupMap["sumo_tlc_set_ryg_state_server"];
  ros::AdvertiseServiceOptions sumo_tlc_set_ryg_state_server_server_options;
  sumo_tlc_set_ryg_state_server_server_options = ros::AdvertiseServiceOptions::create<dsc::sumo_tlc_set_ryg_state>
      (advertiseName.c_str(),
       boost::bind(&sumo_intf::sumo_tlc_set_ryg_stateCallback, this, _1, _2),
       ros::VoidPtr(),
       &this->compQueue);
  this->sumo_tlc_set_ryg_state_server = nh.advertiseService(sumo_tlc_set_ryg_state_server_server_options);  
 
  // Init Timer
  ros::TimerOptions timer_options;
  timer_options = 
    ros::TimerOptions
    (ros::Duration(-1),
     boost::bind(&sumo_intf::Init, this, _1),
     &this->compQueue,
     true,
     false);
  this->initOneShotTimer = nh.createTimer(timer_options);
  this->initOneShotTimer.stop();
  // Component Timer - sumo_step_timer
  timer_options = 
    ros::TimerOptions
    (ros::Duration(0.1),
     boost::bind(&sumo_intf::sumo_step_timerCallback, this, _1),
     &this->compQueue, false, false);
  this->sumo_step_timer = nh.createTimer(timer_options);

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
  std::string log_file_path = pwd + nodeName + "." + compName + ".log"; 
  
  // Create the log file & open file stream
  LOGGER.CREATE_FILE(log_file_path);
  
  // Establish log levels of LOGGER
  LOGGER.SET_LOG_LEVELS(logLevels);


  this->comp_sync_pub = nh.advertise<std_msgs::Bool>("component_synchronization", 1000);
  
  ros::SubscribeOptions comp_sync_sub_options;
  comp_sync_sub_options = ros::SubscribeOptions::create<std_msgs::Bool>
    ("component_synchronization",
     1000,
     boost::bind(&sumo_intf::component_synchronization_OnOneData, this, _1),
     ros::VoidPtr(),
     &this->compQueue);
  this->comp_sync_sub = nh.subscribe(comp_sync_sub_options);

  ros::Time now = ros::Time::now();
  while ( this->comp_sync_sub.getNumPublishers() < this->num_comps_to_sync &&
	  (ros::Time::now() - now) < ros::Duration(comp_sync_timeout) )
    ros::Duration(0.1).sleep();
  ros::Duration(0.5).sleep();
  this->comp_sync_sub.shutdown();
  this->comp_sync_pub.shutdown();

  this->initOneShotTimer.start();
  this->sumo_step_timer.start();
  
}

extern "C" {
  Component *maker(ComponentConfig &config, int argc, char **argv) {
    return new sumo_intf(config,argc,argv);
  }
}
