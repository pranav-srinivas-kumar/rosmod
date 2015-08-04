#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <stdio.h>
#include <map>

#include "boost/filesystem.hpp"

#include "node/rapidxml.hpp"
#include "node/rapidxml_utils.hpp"
#include "node/Logger.hpp"

class ComponentConfig
{
public:
  std::string libraryLocation;
  std::string schedulingScheme;
  std::string hostName;
  std::string nodeName;
  std::string compName;
  std::map<std::string,std::string> portGroupMap;
  Log_Levels logLevels;
  uint64_t num_comps_to_sync;
  double comp_sync_timeout;
  double tg_time;
  uint64_t oob_uuid;
  std::string profileName;
};

using namespace rapidxml;

class XMLParser
{
public:
  std::vector<ComponentConfig> compConfigList;
  std::vector<std::string> libList;
  std::string nodeName;

  bool Return_Boolean(std::string value) { return (value == "True"); }

  void PrintNode(xml_node<> *node, std::string& prepend)
  {
    std::string local_prepend = prepend;
    printf("%s%s:\n",local_prepend.c_str(),node->name());
    for (xml_attribute<> *tmpAttr = node->first_attribute();
	 tmpAttr; tmpAttr = tmpAttr->next_attribute())
      {
	printf("%s\t%s: %s\n",
	       local_prepend.c_str(),
	       tmpAttr->name(),
	       tmpAttr->value());
      }
    local_prepend += "\t";
    for (xml_node<> *tmpNode = node->first_node();
	 tmpNode; tmpNode = tmpNode->next_sibling())
      {
	PrintNode(tmpNode, local_prepend);
      }
  }

  bool Parse(std::string fName)
  {
    if (!boost::filesystem::exists(fName))
      return false;
    rapidxml::file<> xmlFile(fName.c_str());
    rapidxml::xml_document<> doc;
    doc.parse<0>(xmlFile.data());

    xml_node<> *node = doc.first_node("node");
    nodeName = node->first_attribute()->value();
    
    for (xml_node<> *lib_location = node->first_node("library");
	 lib_location; lib_location = lib_location->next_sibling("library"))
      {
	libList.push_back(lib_location->first_attribute()->value());
      }

    for (xml_node<> *comp_inst = node->first_node("component_instance"); 
	 comp_inst; comp_inst = comp_inst->next_sibling("component_instance"))
      {
	ComponentConfig config;
	config.num_comps_to_sync = 1;
	config.comp_sync_timeout = 1.0;
	config.compName = comp_inst->first_attribute()->value();
	config.nodeName = nodeName;

	xml_node<> *nCompsSync = comp_inst->first_node("numCompsToSync");
	if (nCompsSync != NULL)
	  config.num_comps_to_sync = atoi(nCompsSync->first_attribute()->value());
	
	xml_node<> *syncTimeout = comp_inst->first_node("syncTimeout");
	if (syncTimeout != NULL)
	  config.comp_sync_timeout = atof(syncTimeout->first_attribute()->value());
	
	xml_node<> *oob_uuid = comp_inst->first_node("oob_uuid");
	if (oob_uuid != NULL)
	  config.oob_uuid = atoi(oob_uuid->first_attribute()->value());
	
	xml_node<> *profileName = comp_inst->first_node("profileName");
	if (profileName != NULL)
	  config.profileName = profileName->first_attribute()->value();
	
	xml_node<> *tg_time = comp_inst->first_node("tg_time");
	if (tg_time != NULL)
	  config.tg_time = atof(tg_time->first_attribute()->value());
	
	xml_node<> *lib_location = comp_inst->first_node("library");
	config.libraryLocation = lib_location->first_attribute()->value();
	
	xml_node<> *sched_scheme = comp_inst->first_node("scheduling_scheme");
	config.schedulingScheme = sched_scheme->first_attribute()->value();
	
	xml_node<> *logger = comp_inst->first_node("logging");
	config.logLevels.DEBUG = 
	  Return_Boolean(logger->first_node("debug")->first_attribute()->value());
	config.logLevels.INFO = 
	  Return_Boolean(logger->first_node("info")->first_attribute()->value());
	config.logLevels.WARNING = 
	  Return_Boolean(logger->first_node("warning")->first_attribute()->value());
	config.logLevels.ERROR = 
	  Return_Boolean(logger->first_node("error")->first_attribute()->value());
	config.logLevels.CRITICAL = 
	  Return_Boolean(logger->first_node("critical")->first_attribute()->value());
	
	for (xml_node<> *port_inst = comp_inst->first_node("port_instance"); 
	     port_inst; port_inst = port_inst->next_sibling("port_instance"))
	  {
	    std::string portInstName = port_inst->first_attribute()->value();
	    xml_node<> *port = port_inst->first_node("port");
	    std::string portName = port->first_attribute()->value();
	    xml_node<> *group = port_inst->first_node("group");
	    std::string groupID = group->first_attribute()->value();
	    config.portGroupMap.insert(std::pair<std::string,std::string>(portName,groupID));
	  }
	compConfigList.push_back(config);
      }
    return true;
  }
};



