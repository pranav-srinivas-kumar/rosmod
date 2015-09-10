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
__CHEETAH_genTime__ = 1441894812.958882
__CHEETAH_genTimestamp__ = 'Thu Sep 10 09:20:12 2015'
__CHEETAH_src__ = '/home/jeb/Repositories/rosmod-gui/src/rosmod_v0.3/templates/base_component_cpp.tmpl'
__CHEETAH_srcLastModified__ = 'Tue Aug  4 13:43:47 2015'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class base_component_cpp(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(base_component_cpp, self).__init__(*args, **KWs)
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
        
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 1, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 1, col 1.
        write(u''' "''')
        _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 1, col 16
        if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 1, col 16.
        write(u'''/Component.hpp"

// Constructor
Component::Component(ComponentConfig &_config, int argc, char **argv) {
  this->config = _config;
  portGroupMap = config.portGroupMap;
  logLevels = config.logLevels;
  hostName = config.hostName;
  nodeName = config.nodeName;
  compName = config.compName;
  node_argc = argc;
  node_argv = argv;
  num_comps_to_sync = config.num_comps_to_sync;
  comp_sync_timeout = config.comp_sync_timeout;
''')
        if VFFSL(SL,"mod",True) != "": # generated from line 15, col 1
            write(u'''  if (config.schedulingScheme == "FIFO")
    scheduling_scheme = rosmod::CallbackQueue::SchedulingScheme::FIFO;
  else if (config.schedulingScheme == "PFIFO")
    scheduling_scheme = rosmod::CallbackQueue::SchedulingScheme::PFIFO;
  else if (config.schedulingScheme == "EDF")
    scheduling_scheme = rosmod::CallbackQueue::SchedulingScheme::EDF;
''')
        write(u'''}

// Destructor
Component::~Component() {
  compQueue.disable();
  initOneShotTimer.stop();
}

// Initialization
void Component::Init(const ros''')
        _v = VFFSL(SL,"mod",True) # u'${mod}' on line 32, col 31
        if _v is not None: write(_filter(_v, rawExpr=u'${mod}')) # from line 32, col 31.
        write(u'''::TimerEvent& event) {}

// Synchronization
void Component::component_synchronization_OnOneData(const std_msgs::Bool::ConstPtr& received_data) {}

// Callback Queue Handler
void Component::processQueue() {  
  ros''')
        _v = VFFSL(SL,"mod",True) # u'${mod}' on line 39, col 6
        if _v is not None: write(_filter(_v, rawExpr=u'${mod}')) # from line 39, col 6.
        write(u'''::NodeHandle nh;
  while (nh.ok()) {
    this->compQueue.callAvailable(ros::WallDuration(0.01));
  }
}
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

    _mainCheetahMethod_for_base_component_cpp= 'respond'

## END CLASS DEFINITION

if not hasattr(base_component_cpp, '_initCheetahAttributes'):
    templateAPIClass = getattr(base_component_cpp, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(base_component_cpp)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=base_component_cpp()).run()


