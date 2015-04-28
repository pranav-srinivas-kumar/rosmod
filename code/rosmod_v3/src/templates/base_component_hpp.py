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
__CHEETAH_genTime__ = 1430196875.038399
__CHEETAH_genTimestamp__ = 'Mon Apr 27 23:54:35 2015'
__CHEETAH_src__ = '/home/kelsier/Repositories/rosmod/code/rosmod_v3/src/templates/base_component_hpp.tmpl'
__CHEETAH_srcLastModified__ = 'Sun Apr 19 17:15:22 2015'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class base_component_hpp(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(base_component_hpp, self).__init__(*args, **KWs)
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
        
        write(u'''\ufeff#ifndef COMPONENT_HPP
#define COMPONENT_HPP

''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 4, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 4, col 1.
        write(u''' <iostream>
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 5, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 5, col 1.
        write(u''' <string>
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 6, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 6, col 1.
        write(u''' "ros/ros.h"
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 7, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 7, col 1.
        write(u''' <ros/callback_queue.h>
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 8, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 8, col 1.
        write(u''' "''')
        _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 8, col 16
        if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 8, col 16.
        write(u'''/xmlParser.hpp"
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 9, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 9, col 1.
        write(u''' "''')
        _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 9, col 16
        if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 9, col 16.
        write(u'''/Logger.hpp"

class Component
{
    public:
        // Component Constructor
        Component(std::string hostName, std::string nodeName, std::string compName, int argc, char **argv);

\t// StartUp will be completely generated
\tvirtual void startUp() = 0;

\t// Init will be generated with BL supplied by user
\tvirtual void Init(const ros::TimerEvent& event);

\t// queueThread processes queue actions
\tvoid processQueue();

\t// required for clean shutdown
\t~Component();

    protected:
        std::string hostName;
        std::string nodeName;
        std::string compName;
        int node_argc;
        char **node_argv;
\tros::Timer initOneShotTimer;  // timer for calling init
\tros::CallbackQueue compQueue; // single callbackQueue for the component
        Logger LOGGER;
};

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

    _mainCheetahMethod_for_base_component_hpp= 'respond'

## END CLASS DEFINITION

if not hasattr(base_component_hpp, '_initCheetahAttributes'):
    templateAPIClass = getattr(base_component_hpp, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(base_component_hpp)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=base_component_hpp()).run()


