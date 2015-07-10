#!/usr/bin/env python




##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.4.4'
__CHEETAH_versionTuple__ = (2, 4, 4, 'development', 0)
__CHEETAH_genTime__ = 1436565893.464405
__CHEETAH_genTimestamp__ = 'Fri Jul 10 17:04:53 2015'
__CHEETAH_src__ = '/home/jeb/Repositores/rosmod/src/rosmod_v0.3/templates/CMakeLists.tmpl'
__CHEETAH_srcLastModified__ = 'Fri Jul 10 14:22:02 2015'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class CMakeLists(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(CMakeLists, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''cmake_minimum_required(VERSION 2.8.3)
project(''')
        _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 2, col 9
        if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 2, col 9.
        write(u''')

''')
        if VFFSL(SL,"functions",True) == "": # generated from line 4, col 1
            write(u'''## Start Global Marker

## End Global Marker
''')
        else: # generated from line 8, col 1
            write(u'''## Start Global Marker
''')
            _v = VFFSL(SL,"functions",True) # u'$functions' on line 10, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$functions')) # from line 10, col 1.
            write(u'''## End Global Marker
''')
        write(u'''
## Check C++11 / C++0x
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)
if(COMPILER_SUPPORTS_CXX11)
    set(CMAKE_CXX_FLAGS "-std=c++11")
elseif(COMPILER_SUPPORTS_CXX0X)
    set(CMAKE_CXX_FLAGS "-std=c++0x")
else()
    message(FATAL_ERROR "The compiler ''')
        _v = VFFSL(SL,"CMAKE_CXX_COMPILER",True) # u'${CMAKE_CXX_COMPILER}' on line 22, col 39
        if _v is not None: write(_filter(_v, rawExpr=u'${CMAKE_CXX_COMPILER}')) # from line 22, col 39.
        write(u''' has no C++11 support. Please use a different C++ compiler.")
endif()

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
roscpp
std_msgs
message_generation
''')
        if VFFSL(SL,"packages",True) == "": # generated from line 32, col 1
            write(u'''## Start Package Marker
## End Package Marker
''')
        else: # generated from line 35, col 1
            write(u'''## Start Package Marker
''')
            _v = VFFSL(SL,"packages",True) # u'$packages' on line 37, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$packages')) # from line 37, col 1.
            write(u'''## End Package Marker
''')
        write(u''')

## System dependencies are found with CMake\'s conventions
# find_package(Boost REQUIRED COMPONENTS system)


## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
# catkin_python_setup()

#
## Declare ROS messages, services and actions 
#

## To declare and build messages, services or actions from within this
## package, follow these steps:
## * Let MSG_DEP_SET be the set of packages whose message types you use in
##   your messages/services/actions (e.g. std_msgs, actionlib_msgs, ...).
## * In the file package.xml:
##   * add a build_depend and a run_depend tag for each package in MSG_DEP_SET
##   * If MSG_DEP_SET isn\'t empty the following dependencies might have been
##     pulled in transitively but can be declared for certainty nonetheless:
##     * add a build_depend tag for "message_generation"
##     * add a run_depend tag for "message_runtime"
## * In this file (CMakeLists.txt):
##   * add "message_generation" and every package in MSG_DEP_SET to
##     find_package(catkin REQUIRED COMPONENTS ...)
##   * add "message_runtime" and every package in MSG_DEP_SET to
##     catkin_package(CATKIN_DEPENDS ...)
##   * uncomment the add_*_files sections below as needed
##     and list every .msg/.srv/.action file to be processed
##   * uncomment the generate_messages entry below
##   * add every package in MSG_DEP_SET to generate_messages(DEPENDENCIES ...)

# Generate messages in the \'msg\' folder
''')
        if VFFSL(SL,"messages",True) != []: # generated from line 75, col 1
            write(u'''add_message_files(
  FILES
''')
            for msg in VFFSL(SL,"messages",True): # generated from line 78, col 1
                write(u'''  ''')
                _v = VFN(VFFSL(SL,"msg",True),"properties",True)["name"] # u'${msg.properties["name"]}' on line 79, col 3
                if _v is not None: write(_filter(_v, rawExpr=u'${msg.properties["name"]}')) # from line 79, col 3.
                write(u'''.msg

''')
            write(u''')
''')
        write(u"""
# Generate services in the 'srv' folder
""")
        if VFFSL(SL,"services",True) != []: # generated from line 86, col 1
            write(u'''add_service_files(
  FILES
''')
            for srv in VFFSL(SL,"services",True): # generated from line 89, col 1
                write(u'''  ''')
                _v = VFN(VFFSL(SL,"srv",True),"properties",True)["name"] # u'${srv.properties["name"]}' on line 90, col 3
                if _v is not None: write(_filter(_v, rawExpr=u'${srv.properties["name"]}')) # from line 90, col 3.
                write(u'''.srv

''')
            write(u''')
''')
        write(u"""
## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

# Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  std_msgs
)

#
## catkin specific configuration 
#
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if you package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES """)
        _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 120, col 14
        if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 120, col 14.
        write(u'''
#  CATKIN_DEPENDS roscpp std_msgs
  CATKIN_DEPENDS message_runtime
#  DEPENDS system_lib
)

#
## Build 
#

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  ''')
        _v = VFFSL(SL,"catkin_INCLUDE_DIRS",True) # u'${catkin_INCLUDE_DIRS}' on line 134, col 3
        if _v is not None: write(_filter(_v, rawExpr=u'${catkin_INCLUDE_DIRS}')) # from line 134, col 3.
        write(u'''
''')
        if VFFSL(SL,"include_dirs",True) == "": # generated from line 135, col 1
            write(u'''## Start Include Directories Marker
## End Include Directories Marker
''')
        else: # generated from line 138, col 1
            write(u'''## Start Include Directories Marker
''')
            _v = VFFSL(SL,"include_dirs",True) # u'$include_dirs' on line 140, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$include_dirs')) # from line 140, col 1.
            write(u'''## End Include Directories Marker
''')
        write(u''')

## Declare a cpp library
# add_library(''')
        _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 145, col 15
        if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 145, col 15.
        write(u'''
#   src/''')
        _v = VFFSL(SL,"PROJECT_NAME",True) # u'${PROJECT_NAME}' on line 146, col 9
        if _v is not None: write(_filter(_v, rawExpr=u'${PROJECT_NAME}')) # from line 146, col 9.
        write(u'''/''')
        _v = VFFSL(SL,"package_name",True) # u'${package_name}' on line 146, col 25
        if _v is not None: write(_filter(_v, rawExpr=u'${package_name}')) # from line 146, col 25.
        write(u'''.cpp
# )

## Declare a cpp executable
# add_executable(''')
        _v = VFFSL(SL,"package_name",True) # u'${package_name}' on line 150, col 18
        if _v is not None: write(_filter(_v, rawExpr=u'${package_name}')) # from line 150, col 18.
        write(u'''_node src/''')
        _v = VFFSL(SL,"package_name",True) # u'${package_name}' on line 150, col 43
        if _v is not None: write(_filter(_v, rawExpr=u'${package_name}')) # from line 150, col 43.
        write(u'''_node.cpp)

## Add cmake target dependencies of the executable/library
## as an example, message headers may need to be generated before nodes
# add_dependencies(''')
        _v = VFFSL(SL,"package_name",True) # u'${package_name}' on line 154, col 20
        if _v is not None: write(_filter(_v, rawExpr=u'${package_name}')) # from line 154, col 20.
        write(u'''_node ''')
        _v = VFFSL(SL,"package_name",True) # u'${package_name}' on line 154, col 41
        if _v is not None: write(_filter(_v, rawExpr=u'${package_name}')) # from line 154, col 41.
        write(u'''_generate_messages_cpp)

## Specify libraries to link a library or executable target against
# target_link_libraries(''')
        _v = VFFSL(SL,"package_name",True) # u'${package_name}' on line 157, col 25
        if _v is not None: write(_filter(_v, rawExpr=u'${package_name}')) # from line 157, col 25.
        write(u'''_node
#   ''')
        _v = VFFSL(SL,"catkin_LIBRARIES",True) # u'${catkin_LIBRARIES}' on line 158, col 5
        if _v is not None: write(_filter(_v, rawExpr=u'${catkin_LIBRARIES}')) # from line 158, col 5.
        write(u'''
# )

#
## Install 
#

# all install targets should use catkin DESTINATION variables
# See http://ros.org/doc/api/catkin/html/adv_user_guide/variables.html

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
# install(PROGRAMS
#   scripts/my_python_script
#   DESTINATION ''')
        _v = VFFSL(SL,"CATKIN_PACKAGE_BIN_DESTINATION",True) # u'${CATKIN_PACKAGE_BIN_DESTINATION}' on line 172, col 17
        if _v is not None: write(_filter(_v, rawExpr=u'${CATKIN_PACKAGE_BIN_DESTINATION}')) # from line 172, col 17.
        write(u'''
# )

## Mark executables and/or libraries for installation
# install(TARGETS ''')
        _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 176, col 19
        if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 176, col 19.
        write(u''' ''')
        _v = VFFSL(SL,"package_name",True) # u'${package_name}' on line 176, col 33
        if _v is not None: write(_filter(_v, rawExpr=u'${package_name}')) # from line 176, col 33.
        write(u'''_node
#   ARCHIVE DESTINATION ''')
        _v = VFFSL(SL,"CATKIN_PACKAGE_LIB_DESTINATION",True) # u'${CATKIN_PACKAGE_LIB_DESTINATION}' on line 177, col 25
        if _v is not None: write(_filter(_v, rawExpr=u'${CATKIN_PACKAGE_LIB_DESTINATION}')) # from line 177, col 25.
        write(u'''
#   LIBRARY DESTINATION ''')
        _v = VFFSL(SL,"CATKIN_PACKAGE_LIB_DESTINATION",True) # u'${CATKIN_PACKAGE_LIB_DESTINATION}' on line 178, col 25
        if _v is not None: write(_filter(_v, rawExpr=u'${CATKIN_PACKAGE_LIB_DESTINATION}')) # from line 178, col 25.
        write(u'''
#   RUNTIME DESTINATION ''')
        _v = VFFSL(SL,"CATKIN_PACKAGE_BIN_DESTINATION",True) # u'${CATKIN_PACKAGE_BIN_DESTINATION}' on line 179, col 25
        if _v is not None: write(_filter(_v, rawExpr=u'${CATKIN_PACKAGE_BIN_DESTINATION}')) # from line 179, col 25.
        write(u'''
# )

## Mark cpp header files for installation
# install(DIRECTORY include/''')
        _v = VFFSL(SL,"PROJECT_NAME",True) # u'${PROJECT_NAME}' on line 183, col 29
        if _v is not None: write(_filter(_v, rawExpr=u'${PROJECT_NAME}')) # from line 183, col 29.
        write(u'''/
#   DESTINATION ''')
        _v = VFFSL(SL,"CATKIN_PACKAGE_INCLUDE_DESTINATION",True) # u'${CATKIN_PACKAGE_INCLUDE_DESTINATION}' on line 184, col 17
        if _v is not None: write(_filter(_v, rawExpr=u'${CATKIN_PACKAGE_INCLUDE_DESTINATION}')) # from line 184, col 17.
        write(u'''
#   FILES_MATCHING PATTERN "*.h"
#   PATTERN ".svn" EXCLUDE
# )

## Mark other files for installation (e.g. launch and bag files, etc.)
# install(FILES
#   # myfile1
#   # myfile2
#   DESTINATION ''')
        _v = VFFSL(SL,"CATKIN_PACKAGE_SHARE_DESTINATION",True) # u'${CATKIN_PACKAGE_SHARE_DESTINATION}' on line 193, col 17
        if _v is not None: write(_filter(_v, rawExpr=u'${CATKIN_PACKAGE_SHARE_DESTINATION}')) # from line 193, col 17.
        write(u'''
# )

#
## Testing 
#

## Add gtest based cpp test target and link libraries
# catkin_add_gtest(''')
        _v = VFFSL(SL,"PROJECT_NAME",True) # u'${PROJECT_NAME}' on line 201, col 20
        if _v is not None: write(_filter(_v, rawExpr=u'${PROJECT_NAME}')) # from line 201, col 20.
        write(u'''-test test/test_''')
        _v = VFFSL(SL,"package_name",True) # u'${package_name}' on line 201, col 51
        if _v is not None: write(_filter(_v, rawExpr=u'${package_name}')) # from line 201, col 51.
        write(u'''.cpp)
# if(TARGET ''')
        _v = VFFSL(SL,"PROJECT_NAME",True) # u'${PROJECT_NAME}' on line 202, col 13
        if _v is not None: write(_filter(_v, rawExpr=u'${PROJECT_NAME}')) # from line 202, col 13.
        write(u'''-test)
#   target_link_libraries(''')
        _v = VFFSL(SL,"PROJECT_NAME",True) # u'${PROJECT_NAME}' on line 203, col 27
        if _v is not None: write(_filter(_v, rawExpr=u'${PROJECT_NAME}')) # from line 203, col 27.
        write(u'''-test ''')
        _v = VFFSL(SL,"PROJECT_NAME",True) # u'${PROJECT_NAME}' on line 203, col 48
        if _v is not None: write(_filter(_v, rawExpr=u'${PROJECT_NAME}')) # from line 203, col 48.
        write(u''')
# endif()

## Add folders to be run by python nosetests
# catkin_add_nosetests(test)
include_directories(include ''')
        _v = VFFSL(SL,"catkin_INCLUDE_DIRS",True) # u'${catkin_INCLUDE_DIRS}' on line 208, col 29
        if _v is not None: write(_filter(_v, rawExpr=u'${catkin_INCLUDE_DIRS}')) # from line 208, col 29.
        write(u''')

''')
        if VFFSL(SL,"components",True) != []: # generated from line 210, col 1
            for component in VFFSL(SL,"components",True): # generated from line 211, col 1
                write(u'''add_library(''')
                _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'${component.properties["name"]}' on line 212, col 13
                if _v is not None: write(_filter(_v, rawExpr=u'${component.properties["name"]}')) # from line 212, col 13.
                write(u'''
            src/''')
                _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 213, col 17
                if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 213, col 17.
                write(u'''/''')
                _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'${component.properties["name"]}' on line 213, col 31
                if _v is not None: write(_filter(_v, rawExpr=u'${component.properties["name"]}')) # from line 213, col 31.
                write(u'''.cpp
''')
                if VFN(VFFSL(SL,"component",True),"properties",True)["cmakelists_cpp_marker"] != "": # generated from line 214, col 1
                    write(u'''            ## Start ''')
                    _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'$component.properties["name"]' on line 215, col 23
                    if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["name"]')) # from line 215, col 23.
                    write(u''' CPP Marker
''')
                    _v = VFN(VFFSL(SL,"component",True),"properties",True)["cmakelists_cpp_marker"] # u'$component.properties["cmakelists_cpp_marker"]' on line 216, col 1
                    if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["cmakelists_cpp_marker"]')) # from line 216, col 1.
                    write(u'''            ## End ''')
                    _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'$component.properties["name"]' on line 216, col 67
                    if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["name"]')) # from line 216, col 67.
                    write(u''' CPP Marker
''')
                else: # generated from line 217, col 1
                    write(u'''            ## Start ''')
                    _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'$component.properties["name"]' on line 218, col 23
                    if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["name"]')) # from line 218, col 23.
                    write(u''' CPP Marker

            ## End ''')
                    _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'$component.properties["name"]' on line 220, col 21
                    if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["name"]')) # from line 220, col 21.
                    write(u''' CPP Marker
''')
                write(u'''           )
target_link_libraries(''')
                _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'${component.properties["name"]}' on line 223, col 23
                if _v is not None: write(_filter(_v, rawExpr=u'${component.properties["name"]}')) # from line 223, col 23.
                write(u'''
''')
                if VFN(VFFSL(SL,"component",True),"properties",True)["cmakelists_targetlinklibs_marker"] != "": # generated from line 224, col 1
                    write(u'''                      ## Start ''')
                    _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'$component.properties["name"]' on line 225, col 33
                    if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["name"]')) # from line 225, col 33.
                    write(u''' Target Link Libraries Marker
''')
                    _v = VFN(VFFSL(SL,"component",True),"properties",True)["cmakelists_targetlinklibs_marker"] # u'$component.properties["cmakelists_targetlinklibs_marker"]' on line 226, col 1
                    if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["cmakelists_targetlinklibs_marker"]')) # from line 226, col 1.
                    write(u'''                      ## End ''')
                    _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'$component.properties["name"]' on line 226, col 88
                    if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["name"]')) # from line 226, col 88.
                    write(u''' Target Link Libraries Marker
''')
                else: # generated from line 227, col 1
                    write(u'''                      ## Start ''')
                    _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'$component.properties["name"]' on line 228, col 33
                    if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["name"]')) # from line 228, col 33.
                    write(u''' Target Link Libraries Marker

                      ## End ''')
                    _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'$component.properties["name"]' on line 230, col 31
                    if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["name"]')) # from line 230, col 31.
                    write(u''' Target Link Libraries Marker
''')
                write(u'''                      ''')
                _v = VFFSL(SL,"catkin_LIBRARIES",True) # u'${catkin_LIBRARIES}' on line 232, col 23
                if _v is not None: write(_filter(_v, rawExpr=u'${catkin_LIBRARIES}')) # from line 232, col 23.
                write(u'''
                      )
add_dependencies(''')
                _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'${component.properties["name"]}' on line 234, col 18
                if _v is not None: write(_filter(_v, rawExpr=u'${component.properties["name"]}')) # from line 234, col 18.
                write(u'''
                 ''')
                _v = VFFSL(SL,"package_name",True) # u'${package_name}' on line 235, col 18
                if _v is not None: write(_filter(_v, rawExpr=u'${package_name}')) # from line 235, col 18.
                write(u'''_generate_messages_cpp
                )

''')
        if VFFSL(SL,"needs_io",True): # generated from line 240, col 1
            write(u'''add_library(KRPCI
            src/krpci/KRPC.pb.cc
\t    src/krpci/krpci_base.cpp
            src/krpci/krpci_generated.cpp
\t    )
target_link_libraries(KRPCI
  boost_system boost_thread /usr/lib/libprotobuf.so.10
  )
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_CMakeLists= 'respond'

## END CLASS DEFINITION

if not hasattr(CMakeLists, '_initCheetahAttributes'):
    templateAPIClass = getattr(CMakeLists, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(CMakeLists)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=CMakeLists()).run()


