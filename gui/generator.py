# ROSMOD Generator
# Author: Pranav Srinivas Kumar
# Date: 2015.02.28

from Cheetah.Template import Template
import os, sys, inspect
from pkg_resources import resource_filename

# Template Compile Step -- Compiling tmpl files in templates
# Generate template python files
generator_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(generator_dir + "/templates")

# Recursively compile on template files in templates directory
os.system("/usr/local/bin/cheetah compile " + template_dir + "/*.tmpl")# > /dev/null 2>&1")
ros_templates = os.path.realpath(os.path.abspath
                                 (os.path.join
                                  (os.path.split
                                   (inspect.getfile
                                    (inspect.currentframe()
                                 )
                                )[0], "templates")
                              ))
if ros_templates not in sys.path:
    sys.path.insert(0, ros_templates)
from package_xml import *
from rapidxml_hpp import *
from rapidxml_utils_hpp import *
from xmlParser_hpp import *
from Logger_cpp import *
from Logger_hpp import *
from base_component_hpp import *
from base_component_cpp import *
import msg as msg_template
import srv as srv_template
from component_hpp import *
from component_cpp import *
from nodeMain import *
from CMakeLists import *
from node_CMakeLists import *
from rml import *
from xml import *
import rhw as rhw_template
import rdp as rdp_template

from shutil import *

class ROSMOD_Generator: 
    # Main Generate Function
    def generate_workspace(self, workspace, path, comm, trafficGen):
        mod = ""
        if (comm == "ROSCPP"):
            mod = ""
        elif (comm == "ROSMOD"):
            mod = "mod"
        print "ROSMOD::Generating " + comm + " Workspace..."
        # Make the workspace directory
        # Make the workspace directory
        self.workspace_dir = os.path.join(path, workspace.properties["name"])
        print "ROSMOD::Workspace Path:", self.workspace_dir
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

        # Generate the .catkin_ws file
        catkin_ws = "# This file currently only serves to mark the location of a catkin workspace for tool integration "
        filename = ".catkin_workspace"
        with open(os.path.join(self.workspace_dir, filename), 'w') as temp_file:
            temp_file.write(catkin_ws)
            temp_file.close()  

        # Make the src directory
        self.src_path = self.workspace_dir + "/src"
        if not os.path.exists(self.src_path):
            os.makedirs(self.src_path)  

        # Create the "node" package
        self.node_path = os.path.join(self.src_path, "node")
        print "ROSMOD:: Node Executable Path: " + self.node_path
        if not os.path.exists(self.node_path):
            os.makedirs(self.node_path)

        # Create the include directory
        self.include = self.node_path + "/include"
        if not os.path.exists(self.include):
            os.makedirs(self.include)
                
        # Create the src directory
        self.src = self.node_path + "/src"
        if not os.path.exists(self.src):
            os.makedirs(self.src)

        # Create package.xml
        package_xml_namespace = {'package_name' : "node",
                                 'mod': mod}
        t = package_xml(searchList=[package_xml_namespace])
        self.package_xml = str(t)
        with open(os.path.join(self.node_path, "package.xml"), 'w') as temp_file:
            temp_file.write(self.package_xml)

        # Create CMakeLists.txt
        cmakelists_namespace = {'package_name': "node",
                                'catkin_INCLUDE_DIRS': "${catkin_INCLUDE_DIRS}",
                                'PROJECT_NAME': "${PROJECT_NAME}",
                                'catkin_LIBRARIES': '${catkin_LIBRARIES}',
                                'CATKIN_PACKAGE_BIN_DESTINATION':
                                "${CATKIN_PACKAGE_BIN_DESTINATION}",
                                'CATKIN_PACKAGE_LIB_DESTINATION': 
                                "${CATKIN_PACKAGE_LIB_DESTINATION}",
                                'CATKIN_PACKAGE_INCLUDE_DESTINATION':
                                "${CATKIN_PACKAGE_INCLUDE_DESTINATION}",
                                'CATKIN_PACKAGE_SHARE_DESTINATION':
                                "${CATKIN_PACKAGE_SHARE_DESTINATION}",
                                'CMAKE_CXX_COMPILER': "${CMAKE_CXX_COMPILER}",
                                'mod': mod,
                                'NAMESPACE': "${NAMESPACE}"}
        t = node_CMakeLists(searchList=[cmakelists_namespace])
        self.cmakelists = str(t)
        with open(os.path.join(self.node_path, "CMakeLists.txt"), 'w') as temp_file:
            temp_file.write(self.cmakelists)

        # Create Component.cpp and Component.hpp
        self.cpp = self.src + "/node"
        self.hpp = self.include + "/node"
        base_cpp_namespace = {'hash_include': "#include", 
                              'package_name': "node",
                              'mod': mod}
        base_hpp_namespace = {'hash_include': "#include", 
                              'package_name': "node",
                              'mod': mod}

        if not os.path.exists(self.cpp):
            os.makedirs(self.cpp)
        # Populate Base Component cpp template
        t = base_component_cpp(searchList=[base_cpp_namespace])
        self.base_cpp = str(t)
        # Write Component.cpp
        with open(os.path.join(self.cpp, "Component.cpp"), 'w') as temp_file:
            temp_file.write(self.base_cpp)

        if not os.path.exists(self.hpp):
            os.makedirs(self.hpp)
        # Populate Base Component hpp template
        t = base_component_hpp(searchList=[base_hpp_namespace])
        self.base_hpp = str(t)
        # Write Component.hpp
        with open(os.path.join(self.hpp, "Component.hpp"), 'w') as temp_file:
            temp_file.write(self.base_hpp)

        # Populate Logger hpp template
        t = Logger_hpp(searchList=[base_hpp_namespace])
        self.logger_hpp = str(t)
        # Write Logger.hpp
        with open(os.path.join(self.hpp, "Logger.hpp"), 'w') as temp_file:
            temp_file.write(self.logger_hpp)

        xml_namespace = {'hash_include': "#include", 
                         'package_name': "node"}

        # Main RapidXML file
        t = rapidxml_hpp(searchList=[xml_namespace])
        self.rapidxml_hpp = str(t)
        with open(os.path.join(self.hpp, "rapidxml.hpp"), 'w') as temp_file:
            temp_file.write(self.rapidxml_hpp)

        # RapidXML Utils file
        t = rapidxml_utils_hpp(searchList=[xml_namespace])
        self.rapidxml_utils_hpp = str(t)
        with open(os.path.join(self.hpp, "rapidxml_utils.hpp"), 'w') as temp_file:
            temp_file.write(self.rapidxml_utils_hpp)

        # XML Parser file
        t = xmlParser_hpp(searchList=[xml_namespace])
        self.xmlParser_hpp = str(t)
        with open(os.path.join(self.hpp, "xmlParser.hpp"), 'w') as temp_file:
            temp_file.write(self.xmlParser_hpp)

        node_namespace = {'hash_include' : "#include",
                          'mod': mod}
        t = nodeMain(searchList=[node_namespace])
        self.nodeMain_str = str(t)
        node_filename = "node_main.cpp"
        with open(os.path.join(self.cpp, node_filename), 'w') as temp_file:
            temp_file.write(self.nodeMain_str)

        # For each package in the ros model
        for package in workspace.children:

            # Create the package directory
            self.package_path = os.path.join(self.src_path, package.properties["name"])
            print "ROSMOD::" + package.properties["name"] + " Path: " + self.package_path
            if not os.path.exists(self.package_path):
                os.makedirs(self.package_path)

            # Create the include directory
            self.include = self.package_path + "/include"
            if not os.path.exists(self.include):
                os.makedirs(self.include)
                
            # Create the src directory
            self.src = self.package_path + "/src"
            if not os.path.exists(self.src):
                os.makedirs(self.src)

            needs_io = False
            io_types = []
            for comp in package.getChildrenByKind("Component"):
                if comp.properties['datatype'] in ['KSP','SUMO']:
                    needs_io = True
                    if comp.properties['datatype'] not in io_types:
                        io_types.append(comp.properties['datatype'])

            io_output = {}
            io_output['KSP'] = {
                'include dir' : self.include + '/krpci',
                'src dir' : self.src + '/krpci',
                'files' : [
                    [ 'krpci.src.krpci', 'include dir', 'krpci.hpp' ],
                    [ 'krpci.src.krpci', 'include dir', 'KRPC.pb.h' ],
                    [ 'krpci.src', 'src dir', 'krpci_base.cpp' ],
                    [ 'krpci.src', 'src dir', 'krpci_generated.cpp' ],
                    [ 'krpci.src', 'src dir', 'KRPC.pb.cc' ],
                ],
                'dirs' : []
            }
                        
            io_output['SUMO'] = {
                'include dir' : self.include + '/sumo',
                'src dir' : self.src + '/sumo',
                'files' : [
                    [ 'sumocpp.src', 'include dir', 'config.h' ],
                    [ 'sumocpp.src', 'include dir', 'sumo_client.hpp' ],
                    [ 'sumocpp.src', 'src dir', 'sumo_client.cpp' ],
                ],
                'dirs' : [
                    [ 'sumocpp.src', 'include dir', 'foreign' ],
                    [ 'sumocpp.src', 'include dir', 'traci-server' ],
                    [ 'sumocpp.src', 'include dir', 'utils' ],
                ]
            }
                        
            if needs_io == True:
                for io in io_types:
                    if io in io_output:
                        include_dir = io_output[io]['include dir']
                        src_dir = io_output[io]['src dir']
                        if os.path.exists(include_dir):
                            rmtree(include_dir)
                        os.makedirs(include_dir)
                        if os.path.exists(src_dir):
                            rmtree(src_dir)
                        os.makedirs(src_dir)
                        rosmod_path = str(os.getcwd())
                        for _module, _key, _file in io_output[io]['files']:
                            _dir = include_dir if 'include' in _key else src_dir
                            copyfile(resource_filename(_module, _file), _dir + '/' + _file)
                        for _module, _key, _file in io_output[io]['dirs']:
                            _dir = include_dir if 'include' in _key else src_dir
                            copytree(resource_filename(_module, _file), _dir + '/' + _file)
                                     
            if trafficGen == True:
                self.network_middleware_include = self.include + '/network'
                if not os.path.exists(self.network_middleware_include):
                    os.makedirs(self.network_middleware_include)
                rosmod_path = str(os.getcwd())
                fileList = ['oob.hpp','sender.hpp','receiver.hpp','buffer.hpp','NetworkProfile.hpp','Message.hpp','CSVIterator.hpp']
                for f in fileList:
                    copyfile(resource_filename('network_middleware',f),
                             self.network_middleware_include + '/' + f)

            messages = []
            services = []
            components = []
            nodes = []
            for child in package.children:
                if child.kind == "Message":
                    messages.append(child)
                elif child.kind == "Service":
                    services.append(child)
                elif child.kind == "Component":
                    components.append(child)
                elif child.kind == "Node":
                    nodes.append(child)

            if (len(messages) > 0):
                self.msg = self.package_path + "/msg"
                if not os.path.exists(self.msg):
                    os.makedirs(self.msg)

            # Create the srv directory if there are services
            if (len(services) > 0):
                self.srv = self.package_path + "/srv"
                if not os.path.exists(self.srv):
                    os.makedirs(self.srv)

            # Create package.xml
            package_xml_namespace = {'package_name': package.properties["name"],
                                     'mod': mod}
            t = package_xml(searchList=[package_xml_namespace])
            self.package_xml = str(t)
            with open(os.path.join(self.package_path, "package.xml"), 'w') as temp_file:
                temp_file.write(self.package_xml)

            # Create Component.cpp and Component.hpp
            self.cpp = self.src + "/" + package.properties["name"]
            self.hpp = self.include + "/" + package.properties["name"]

            if not os.path.exists(self.cpp):
                os.makedirs(self.cpp)
            if not os.path.exists(self.hpp):
                os.makedirs(self.hpp)

            # Create all package messages in msg folder
            for message in messages:
                msg_namespace = {'definition': message.properties["definition"]}
                msg_filename = message.properties["name"] + ".msg"
                t = msg_template.msg(searchList=[msg_namespace])
                self.msg_fields = str(t)
                # Write msg file
                with open(os.path.join(self.msg, msg_filename), 'w') as temp_file:
                    temp_file.write(self.msg_fields)

            # Create all package services in srv folder
            for service in services:
                srv_filename = service.properties["name"] + ".srv"
                srv_namespace = {'definition' : service.properties["definition"]}
                t = srv_template.srv(searchList=[srv_namespace])
                self.srv_fields = str(t)
                # Write the srv file
                with open(os.path.join(self.srv, srv_filename), 'w') as temp_file:
                    temp_file.write(self.srv_fields)

            cmakelists_services = services

            # Create a .hpp and .cpp per component definition in package
            for component in components:
                component_name  = component.properties["name"]
                define_guard = component_name.upper()

                # Categorize children of component
                publishers = []
                subscribers = []
                clients = []
                servers = []
                timers = []
                provided_services = []
                required_services = []
                for child in component.children:
                    if child.kind == "Publisher":
                        publishers.append(child)
                    elif child.kind == "Subscriber":
                        if "business_logic" not in child.properties.keys():
                            child.properties["business_logic"] = ""
                        subscribers.append(child)
                    elif child.kind == "Client":
                        clients.append(child)
                        required_service = [child.properties["service_reference"].parent.properties["name"], child.properties["service_reference"].properties["name"]]
                        if required_service not in required_services:
                            required_services.append(required_service)
                    elif child.kind == "Server":
                        if "business_logic" not in child.properties.keys():
                            child.properties["business_logic"] = ""
                        servers.append(child)
                        provided_service = child.properties["service_reference"].properties["name"]
                        if provided_service not in provided_services:
                            provided_services.append(provided_service)
                    elif child.kind == "Timer":
                        if "business_logic" not in child.properties.keys():
                            child.properties["business_logic"] = ""
                        timers.append(child)

                topics = []
                for publisher in publishers:
                    topics.append([publisher.properties["message_reference"].parent.properties["name"], 
                                   publisher.properties["message_reference"].properties["name"]])
                for subscriber in subscribers:
                    topics.append([subscriber.properties["message_reference"].parent.properties["name"], 
                                   subscriber.properties["message_reference"].properties["name"]])
                # topics = OrderedSet(topics)
                services = []
                for client in clients:
                    services.append([client.properties["service_reference"].parent.properties["name"],
                                     client.properties["service_reference"].properties["name"]])
                for server in servers:
                    services.append([server.properties["service_reference"].parent.properties["name"],
                                    server.properties["service_reference"].properties["name"]])
                # services = OrderedSet(services)
                hash_include = "#include"

                probably_uninitialized = ["init_business_logic", 
                                          "user_includes", 
                                          "user_globals", 
                                          "hpp_globals", 
                                          "user_private_variables", 
                                          "destructor",
                                          "cmakelists_cpp_marker",
                                          "cmakelists_targetlinklibs_marker"]
                for prop in probably_uninitialized:
                    if prop not in component.properties.keys():
                        component.properties[prop] = ""

                component_namespace = {'define_guard': define_guard, 
                                       'hash_include': hash_include, 
                                       'package_name': package.properties["name"], 
                                       'topics': topics, 
                                       'services': services, 
                                       'component_name': component.properties["name"],
                                       'init_business_logic': component.properties["init_business_logic"],
                                       'user_includes': component.properties["user_includes"],
                                       'user_globals': component.properties["user_globals"],
                                       'hpp_globals': component.properties["hpp_globals"],
                                       'user_private_variables': component.properties["user_private_variables"],
                                       'destructor': component.properties["destructor"],
                                       'publishers': publishers, 
                                       'subscribers': subscribers, 
                                       'clients': clients,
                                       'servers': servers,
                                       'provided_services': provided_services, 
                                       'required_services': required_services, 
                                       'timers': timers,
                                       'component_type': component.properties['datatype'],
                                       'mod': mod,
                                       'trafficGen': trafficGen}
                t = component_hpp(searchList=[component_namespace])
                self.component_hpp_str = str(t)
                # Write the component hpp file
                hpp_filename = component_name + ".hpp"

                with open(os.path.join(self.hpp, hpp_filename), 'w') as temp_file_h:
                    temp_file_h.write(self.component_hpp_str)

                # GENERATING CPP FILES

                t = component_cpp(searchList=[component_namespace])
                self.component_cpp_str = str(t)
                # Write the component cpp file
                cpp_filename = component_name + ".cpp"

                with open(os.path.join(self.cpp, cpp_filename), 'w') as temp_file:
                    temp_file.write(self.component_cpp_str)

            package_uninitialized = ["cmakelists_packages",
                                     "cmakelists_functions", 
                                     "cmakelists_include_dirs"]
            for prop in package_uninitialized:
                if prop not in package.properties.keys():
                    package.properties[prop] = ""

            cmake_lists_namespace = {'package_name': package.properties["name"],
                                     'packages': package.properties["cmakelists_packages"],
                                     'functions': package.properties["cmakelists_functions"],
                                     'include_dirs': package.properties["cmakelists_include_dirs"],
                                     'messages': messages, 
                                     'services': cmakelists_services, 
                                     'catkin_INCLUDE_DIRS': "${catkin_INCLUDE_DIRS}",
                                     'PROJECT_NAME': "${PROJECT_NAME}",
                                     'catkin_LIBRARIES': '${catkin_LIBRARIES}',
                                     'CATKIN_PACKAGE_BIN_DESTINATION':
                                           "${CATKIN_PACKAGE_BIN_DESTINATION}",
                                     'CATKIN_PACKAGE_LIB_DESTINATION': 
                                           "${CATKIN_PACKAGE_LIB_DESTINATION}",
                                     'CATKIN_PACKAGE_INCLUDE_DESTINATION':
                                           "${CATKIN_PACKAGE_INCLUDE_DESTINATION}",
                                     'CATKIN_PACKAGE_SHARE_DESTINATION':
                                           "${CATKIN_PACKAGE_SHARE_DESTINATION}",
                                     'CMAKE_CXX_COMPILER': "${CMAKE_CXX_COMPILER}",
                                     'components': components,
                                     'needs_io' : needs_io,
                                     'io_types' : io_types,
                                     'mod': mod,
                                     'NAMESPACE': "${NAMESPACE}"}
            t = CMakeLists(searchList=[cmake_lists_namespace])
            self.cmake_lists = str(t)
            # Write CMakeLists file
            with open(os.path.join(self.package_path, "CMakeLists.txt"), 'w') as temp_file:
                temp_file.write(self.cmake_lists)     

        return self.workspace_dir

    def generate_xml(self, deployments, deployment_path,
                     num_comps_to_sync = 1, sync_timeout = 100.0):
        for deployment in deployments:
            deployment_folder = deployment_path + "/" + deployment.properties["name"]
            if not os.path.exists(deployment_folder):
                os.makedirs(deployment_folder)
            xml_folder = deployment_folder + "/xml"
            if not os.path.exists(xml_folder):
                os.makedirs(xml_folder)
            bin_folder = deployment_folder + "/bin"
            if not os.path.exists(bin_folder):
                os.makedirs(bin_folder)
            project = deployment.parent
            port_uuids = {}
            comp_insts = deployment.getChildrenByKind('Component_Instance')
            id = 0
            for ci in comp_insts:
                c = ci.properties['component_reference']
                ports = c.getChildrenByKind('Subscriber')
                ports.extend(c.getChildrenByKind('Publisher'))
                for p in ports:
                    port_uuids["{}_{}_{}".format(ci.parent.properties['name'],ci.properties['name'],p.properties['name'])] = id
                    id += 1
            if num_comps_to_sync == 'all':
                num_comps_to_sync = len(deployment.getChildrenByKind("Component_Instance"))
            else:
                num_comps_to_sync = 1
            for node in deployment.children:
                hardware_folder = xml_folder + "/" + node.properties["hardware_reference"].properties["name"]
                if not os.path.exists(hardware_folder):
                    os.makedirs(hardware_folder)
                xml_filename = node.properties["name"] + ".xml"
                needs_io = False
                for comp_inst in node.children:
                    if comp_inst.properties['component_reference'].properties['datatype'] in ['KSP', 'SUMO']:
                        needs_io = True
                xml_namespace = {'node': node,
                                 'needs_io':needs_io,
                                 'io_type':comp_inst.properties['component_reference'].properties['datatype'],
                                 'project':project,
                                 'port_uuids':port_uuids,
                                 'sync_timeout':sync_timeout,
                                 'num_comps_to_sync':num_comps_to_sync}
                t = xml(searchList=[xml_namespace])
                xml_content = str(t)
                with open(os.path.join(hardware_folder, xml_filename), 'w') as temp_file:
                    temp_file.write(xml_content)       

    def generate_cpn(self, workspace, deployments, deployment_path):
        for deployment in deployments:
            deployment_folder = deployment_path + "/" + deployment.properties["name"]
            if not os.path.exists(deployment_folder):
                os.makedirs(deployment_folder)
            cpn_folder = deployment_folder + "/cpn"
            if not os.path.exists(cpn_folder):
                os.makedirs(cpn_folder)
            # Items required for a complete CPN
            timers = []
            components = []
            for package in workspace.children:
                timers += package.getChildrenByKind("Timer")
                components += package.getChildrenByKind("Component")
            for hardware_instance in deployment.children:
                for node in hardware_instance.children:
                    for component_instance in node.children:
                        pass
                     

