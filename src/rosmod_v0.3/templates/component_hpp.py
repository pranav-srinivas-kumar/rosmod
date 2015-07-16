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
__CHEETAH_genTime__ = 1437060493.414806
__CHEETAH_genTimestamp__ = 'Thu Jul 16 10:28:13 2015'
__CHEETAH_src__ = '/home/jeb/Repositories/rosmod-gui/src/rosmod_v0.3/templates/component_hpp.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Jul 15 12:33:54 2015'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class component_hpp(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(component_hpp, self).__init__(*args, **KWs)
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
        
        write(u'''#ifndef ''')
        _v = VFFSL(SL,"define_guard",True) # u'${define_guard}' on line 1, col 9
        if _v is not None: write(_filter(_v, rawExpr=u'${define_guard}')) # from line 1, col 9.
        write(u'''_HPP
#define ''')
        _v = VFFSL(SL,"define_guard",True) # u'${define_guard}' on line 2, col 9
        if _v is not None: write(_filter(_v, rawExpr=u'${define_guard}')) # from line 2, col 9.
        write(u'''_HPP
''')
        if VFFSL(SL,"mod",True) != "": # generated from line 3, col 1
            _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 4, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 4, col 1.
            write(u''' "rosmod/rosmod_ros.h"
''')
        else: # generated from line 5, col 1
            _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 6, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 6, col 1.
            write(u''' "ros/ros.h"
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 8, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 8, col 1.
        write(u''' "Component.hpp"
''')
        for topic in VFFSL(SL,"topics",True): # generated from line 9, col 1
            _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 10, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 10, col 1.
            write(u''' "''')
            _v = VFFSL(SL,"topic",True)[0] # u'$topic[0]' on line 10, col 16
            if _v is not None: write(_filter(_v, rawExpr=u'$topic[0]')) # from line 10, col 16.
            write(u'''/''')
            _v = VFFSL(SL,"topic",True)[1] # u'${topic[1]}' on line 10, col 26
            if _v is not None: write(_filter(_v, rawExpr=u'${topic[1]}')) # from line 10, col 26.
            write(u'''.h"
''')
        for service in VFFSL(SL,"services",True): # generated from line 12, col 1
            _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 13, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 13, col 1.
            write(u''' "''')
            _v = VFFSL(SL,"service",True)[0] # u'$service[0]' on line 13, col 16
            if _v is not None: write(_filter(_v, rawExpr=u'$service[0]')) # from line 13, col 16.
            write(u'''/''')
            _v = VFFSL(SL,"service",True)[1] # u'${service[1]}' on line 13, col 28
            if _v is not None: write(_filter(_v, rawExpr=u'${service[1]}')) # from line 13, col 28.
            write(u'''.h"
''')
        write(u'''
''')
        if VFFSL(SL,"component_type",True) == 'KSP': # generated from line 16, col 1
            _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 17, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 17, col 1.
            write(u''' "krpci/krpci.hpp"
''')
        write(u'''
''')
        if VFFSL(SL,"user_includes",True) == "": # generated from line 20, col 1
            write(u'''//# Start User Includes Marker
//# End User Includes Marker
''')
        else: # generated from line 23, col 1
            write(u'''//# Start User Includes Marker
''')
            _v = VFFSL(SL,"user_includes",True) # u'$user_includes' on line 25, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$user_includes')) # from line 25, col 1.
            write(u'''//# End User Includes Marker
''')
        write(u'''
''')
        if VFFSL(SL,"hpp_globals",True) == "": # generated from line 28, col 1
            write(u'''//# Start User Globals Marker
//# End User Globals Marker
''')
        else: # generated from line 31, col 1
            write(u'''//# Start User Globals Marker
''')
            _v = VFFSL(SL,"hpp_globals",True) # u'$hpp_globals' on line 33, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$hpp_globals')) # from line 33, col 1.
            write(u'''//# End User Globals Marker
''')
        write(u'''
class ''')
        _v = VFFSL(SL,"component_name",True) # u'$component_name' on line 36, col 7
        if _v is not None: write(_filter(_v, rawExpr=u'$component_name')) # from line 36, col 7.
        write(u''' : public Component
{
public:
  // Constructor
  ''')
        _v = VFFSL(SL,"component_name",True) # u'${component_name}' on line 40, col 3
        if _v is not None: write(_filter(_v, rawExpr=u'${component_name}')) # from line 40, col 3.
        write(u'''(ComponentConfig& config, int argc, char **argv) : Component(config, argc, argv) {}

  // Initialization
  void Init(const ros''')
        _v = VFFSL(SL,"mod",True) # u'${mod}' on line 43, col 22
        if _v is not None: write(_filter(_v, rawExpr=u'${mod}')) # from line 43, col 22.
        write(u'''::TimerEvent& event);

''')
        if VFFSL(SL,"len",False)(VFFSL(SL,"subscribers",True)) > 0: # generated from line 45, col 1
            for sub in VFFSL(SL,"subscribers",True): # generated from line 46, col 1
                write(u'''  // Subscriber Callback - ''')
                _v = VFN(VFFSL(SL,"sub",True),"properties",True)["name"] # u'$sub.properties["name"]' on line 47, col 28
                if _v is not None: write(_filter(_v, rawExpr=u'$sub.properties["name"]')) # from line 47, col 28.
                write(u'''
  void ''')
                _v = VFN(VFFSL(SL,"sub",True),"properties",True)["name"] # u'${sub.properties["name"]}' on line 48, col 8
                if _v is not None: write(_filter(_v, rawExpr=u'${sub.properties["name"]}')) # from line 48, col 8.
                write(u'''_OnOneData(const ''')
                _v = VFN(VFN(VFN(VFFSL(SL,"sub",True),"properties",True)["message_reference"],"parent",True),"properties",True)["name"] # u'$sub.properties["message_reference"].parent.properties["name"]' on line 48, col 50
                if _v is not None: write(_filter(_v, rawExpr=u'$sub.properties["message_reference"].parent.properties["name"]')) # from line 48, col 50.
                write(u'''::''')
                _v = VFN(VFN(VFFSL(SL,"sub",True),"properties",True)["message_reference"],"properties",True)["name"] # u'${sub.properties["message_reference"].properties["name"]}' on line 48, col 114
                if _v is not None: write(_filter(_v, rawExpr=u'${sub.properties["message_reference"].properties["name"]}')) # from line 48, col 114.
                write(u'''::ConstPtr& received_data); 
 
''')
        if VFFSL(SL,"len",False)(VFFSL(SL,"provided_services",True)) > 0: # generated from line 52, col 1
            for server in VFFSL(SL,"servers",True): # generated from line 53, col 1
                write(u'''  // Server Callback - ''')
                _v = VFN(VFFSL(SL,"server",True),"properties",True)["name"] # u'$server.properties["name"]' on line 54, col 24
                if _v is not None: write(_filter(_v, rawExpr=u'$server.properties["name"]')) # from line 54, col 24.
                write(u'''
  bool ''')
                _v = VFN(VFN(VFFSL(SL,"server",True),"properties",True)["service_reference"],"properties",True)["name"] # u'${server.properties["service_reference"].properties["name"]}' on line 55, col 8
                if _v is not None: write(_filter(_v, rawExpr=u'${server.properties["service_reference"].properties["name"]}')) # from line 55, col 8.
                write(u'''Callback(''')
                _v = VFN(VFN(VFN(VFFSL(SL,"server",True),"properties",True)["service_reference"],"parent",True),"properties",True)["name"] # u'$server.properties["service_reference"].parent.properties["name"]' on line 55, col 77
                if _v is not None: write(_filter(_v, rawExpr=u'$server.properties["service_reference"].parent.properties["name"]')) # from line 55, col 77.
                write(u'''::''')
                _v = VFN(VFN(VFFSL(SL,"server",True),"properties",True)["service_reference"],"properties",True)["name"] # u'$server.properties["service_reference"].properties["name"]' on line 55, col 144
                if _v is not None: write(_filter(_v, rawExpr=u'$server.properties["service_reference"].properties["name"]')) # from line 55, col 144.
                write(u'''::Request &req, 
    ''')
                _v = VFN(VFN(VFN(VFFSL(SL,"server",True),"properties",True)["service_reference"],"parent",True),"properties",True)["name"] # u'$server.properties["service_reference"].parent.properties["name"]' on line 56, col 5
                if _v is not None: write(_filter(_v, rawExpr=u'$server.properties["service_reference"].parent.properties["name"]')) # from line 56, col 5.
                write(u'''::''')
                _v = VFN(VFN(VFFSL(SL,"server",True),"properties",True)["service_reference"],"properties",True)["name"] # u'$server.properties["service_reference"].properties["name"]' on line 56, col 72
                if _v is not None: write(_filter(_v, rawExpr=u'$server.properties["service_reference"].properties["name"]')) # from line 56, col 72.
                write(u'''::Response &res);

''')
        if VFFSL(SL,"len",False)(VFFSL(SL,"timers",True)) > 0: # generated from line 60, col 1
            for timer in VFFSL(SL,"timers",True): # generated from line 61, col 1
                write(u'''  // Timer Callback - ''')
                _v = VFN(VFFSL(SL,"timer",True),"properties",True)["name"] # u'$timer.properties["name"]' on line 62, col 23
                if _v is not None: write(_filter(_v, rawExpr=u'$timer.properties["name"]')) # from line 62, col 23.
                write(u'''
  void ''')
                _v = VFN(VFFSL(SL,"timer",True),"properties",True)["name"] # u'${timer.properties["name"]}' on line 63, col 8
                if _v is not None: write(_filter(_v, rawExpr=u'${timer.properties["name"]}')) # from line 63, col 8.
                write(u'''Callback(const ros''')
                _v = VFFSL(SL,"mod",True) # u'${mod}' on line 63, col 53
                if _v is not None: write(_filter(_v, rawExpr=u'${mod}')) # from line 63, col 53.
                write(u'''::TimerEvent& event);

''')
        write(u'''  // Start up
  void startUp();

  // Destructor
  ~''')
        _v = VFFSL(SL,"component_name",True) # u'${component_name}' on line 71, col 4
        if _v is not None: write(_filter(_v, rawExpr=u'${component_name}')) # from line 71, col 4.
        write(u'''();

private:

''')
        if VFFSL(SL,"len",False)(VFFSL(SL,"timers",True)) > 0: # generated from line 75, col 1
            for timer in VFFSL(SL,"timers",True): # generated from line 76, col 1
                write(u'''  // Timer
  ros''')
                _v = VFFSL(SL,"mod",True) # u'${mod}' on line 78, col 6
                if _v is not None: write(_filter(_v, rawExpr=u'${mod}')) # from line 78, col 6.
                write(u'''::Timer ''')
                _v = VFN(VFFSL(SL,"timer",True),"properties",True)["name"] # u'$timer.properties["name"]' on line 78, col 20
                if _v is not None: write(_filter(_v, rawExpr=u'$timer.properties["name"]')) # from line 78, col 20.
                write(u''';

''')
        if VFFSL(SL,"len",False)(VFFSL(SL,"subscribers",True)) > 0: # generated from line 82, col 1
            for sub in VFFSL(SL,"subscribers",True): # generated from line 83, col 1
                write(u'''  // Subscriber
  ros''')
                _v = VFFSL(SL,"mod",True) # u'${mod}' on line 85, col 6
                if _v is not None: write(_filter(_v, rawExpr=u'${mod}')) # from line 85, col 6.
                write(u'''::Subscriber ''')
                _v = VFN(VFFSL(SL,"sub",True),"properties",True)["name"] # u'$sub.properties["name"]' on line 85, col 25
                if _v is not None: write(_filter(_v, rawExpr=u'$sub.properties["name"]')) # from line 85, col 25.
                write(u'''; 

''')
        if VFFSL(SL,"len",False)(VFFSL(SL,"publishers",True)) > 0: # generated from line 89, col 1
            for pub in VFFSL(SL,"publishers",True): # generated from line 90, col 1
                write(u'''  // Publisher 
  ros''')
                _v = VFFSL(SL,"mod",True) # u'${mod}' on line 92, col 6
                if _v is not None: write(_filter(_v, rawExpr=u'${mod}')) # from line 92, col 6.
                write(u'''::Publisher ''')
                _v = VFN(VFFSL(SL,"pub",True),"properties",True)["name"] # u'$pub.properties["name"]' on line 92, col 24
                if _v is not None: write(_filter(_v, rawExpr=u'$pub.properties["name"]')) # from line 92, col 24.
                write(u''';

''')
        if VFFSL(SL,"len",False)(VFFSL(SL,"provided_services",True)) > 0: # generated from line 96, col 1
            for server in VFFSL(SL,"servers",True): # generated from line 97, col 1
                write(u'''  // Server 
  ros''')
                _v = VFFSL(SL,"mod",True) # u'${mod}' on line 99, col 6
                if _v is not None: write(_filter(_v, rawExpr=u'${mod}')) # from line 99, col 6.
                write(u'''::ServiceServer ''')
                _v = VFN(VFFSL(SL,"server",True),"properties",True)["name"] # u'${server.properties["name"]}' on line 99, col 28
                if _v is not None: write(_filter(_v, rawExpr=u'${server.properties["name"]}')) # from line 99, col 28.
                write(u''';

''')
        if VFFSL(SL,"len",False)(VFFSL(SL,"required_services",True)) > 0: # generated from line 103, col 1
            for client in VFFSL(SL,"clients",True): # generated from line 104, col 1
                write(u'''  // Client 
  ros''')
                _v = VFFSL(SL,"mod",True) # u'${mod}' on line 106, col 6
                if _v is not None: write(_filter(_v, rawExpr=u'${mod}')) # from line 106, col 6.
                write(u'''::ServiceClient ''')
                _v = VFN(VFFSL(SL,"client",True),"properties",True)["name"] # u'$client.properties["name"]' on line 106, col 28
                if _v is not None: write(_filter(_v, rawExpr=u'$client.properties["name"]')) # from line 106, col 28.
                write(u''';

''')
        if VFFSL(SL,"user_private_variables",True) == "": # generated from line 110, col 1
            write(u'''  //# Start User Private Variables Marker
  //# End User Private Variables Marker
''')
        else: # generated from line 113, col 1
            write(u'''  //# Start User Private Variables Marker
''')
            _v = VFFSL(SL,"user_private_variables",True) # u'$user_private_variables' on line 115, col 1
            if _v is not None: write(_filter(_v, rawExpr=u'$user_private_variables')) # from line 115, col 1.
            write(u'''  //# End User Private Variables Marker
''')
        write(u'''};

#endif
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

    _mainCheetahMethod_for_component_hpp= 'respond'

## END CLASS DEFINITION

if not hasattr(component_hpp, '_initCheetahAttributes'):
    templateAPIClass = getattr(component_hpp, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(component_hpp)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=component_hpp()).run()


