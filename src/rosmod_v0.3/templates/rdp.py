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
__CHEETAH_genTime__ = 1441393768.525612
__CHEETAH_genTimestamp__ = 'Fri Sep  4 14:09:28 2015'
__CHEETAH_src__ = '/home/jeb/Repositories/rosmod-gui/src/rosmod_v0.3/templates/rdp.tmpl'
__CHEETAH_srcLastModified__ = 'Sat Jul 11 17:49:35 2015'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class rdp(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(rdp, self).__init__(*args, **KWs)
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
        
        write(u'''/*
 * ROSMOD Deployment Model
 */

// ROSMOD Hardware Model - ''')
        _v = VFN(VFN(VFSL([locals()]+SL+[globals(), builtin],"deployment",True),"properties",True)["rhw_reference"],"properties",True)["name"] # u'$deployment.properties["rhw_reference"].properties["name"]' on line 5, col 28
        if _v is not None: write(_filter(_v, rawExpr=u'$deployment.properties["rhw_reference"].properties["name"]')) # from line 5, col 28.
        write(u'''
using ''')
        _v = VFN(VFN(VFSL([locals()]+SL+[globals(), builtin],"deployment",True),"properties",True)["rhw_reference"],"properties",True)["name"] # u'$deployment.properties["rhw_reference"].properties["name"]' on line 6, col 7
        if _v is not None: write(_filter(_v, rawExpr=u'$deployment.properties["rhw_reference"].properties["name"]')) # from line 6, col 7.
        write(u''';

''')
        if VFSL([locals()]+SL+[globals(), builtin],"deployment.children",True) != []: # generated from line 8, col 1
            for node in VFSL([locals()]+SL+[globals(), builtin],"deployment.children",True): # generated from line 9, col 1
                write(u'''// ROSMOD Node - ''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"node",True),"properties",True)["name"] # u'$node.properties["name"]' on line 10, col 18
                if _v is not None: write(_filter(_v, rawExpr=u'$node.properties["name"]')) # from line 10, col 18.
                write(u''' 
node ''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"node",True),"properties",True)["name"] # u'$node.properties["name"]' on line 11, col 6
                if _v is not None: write(_filter(_v, rawExpr=u'$node.properties["name"]')) # from line 11, col 6.
                write(u'''
{
  properties
  {
    ref = "''')
                _v = VFN(VFN(VFN(VFSL([locals()]+SL+[globals(), builtin],"node",True),"properties",True)["hardware_reference"],"parent",True),"properties",True)["name"] # u'$node.properties["hardware_reference"].parent.properties["name"]' on line 15, col 12
                if _v is not None: write(_filter(_v, rawExpr=u'$node.properties["hardware_reference"].parent.properties["name"]')) # from line 15, col 12.
                write(u'''/''')
                _v = VFN(VFN(VFSL([locals()]+SL+[globals(), builtin],"node",True),"properties",True)["hardware_reference"],"properties",True)["name"] # u'$node.properties["hardware_reference"].properties["name"]' on line 15, col 77
                if _v is not None: write(_filter(_v, rawExpr=u'$node.properties["hardware_reference"].properties["name"]')) # from line 15, col 77.
                write(u'''";
    priority = ''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"node",True),"properties",True)["priority"] # u'$node.properties["priority"]' on line 16, col 16
                if _v is not None: write(_filter(_v, rawExpr=u'$node.properties["priority"]')) # from line 16, col 16.
                write(u''';
''')
                if VFN(VFSL([locals()]+SL+[globals(), builtin],"node",True),"properties",True)["cmd_args"] != "": # generated from line 17, col 1
                    write(u'''    cmd_args = "''')
                    _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"node",True),"properties",True)["cmd_args"] # u'$node.properties["cmd_args"]' on line 18, col 17
                    if _v is not None: write(_filter(_v, rawExpr=u'$node.properties["cmd_args"]')) # from line 18, col 17.
                    write(u'''";\t\t   
''')
                write(u'''  }
''')
                if VFSL([locals()]+SL+[globals(), builtin],"node.children",True) != []: # generated from line 21, col 1
                    for comp_instance in VFSL([locals()]+SL+[globals(), builtin],"node.children",True): # generated from line 22, col 1
                        write(u'''  component_instance ''')
                        _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["name"] # u'$comp_instance.properties["name"]' on line 23, col 22
                        if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["name"]')) # from line 23, col 22.
                        write(u'''
  {
      properties
      {
\tref = "''')
                        _v = VFN(VFN(VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["component_reference"],"parent",True),"properties",True)["name"] # u'$comp_instance.properties["component_reference"].parent.properties["name"]' on line 27, col 9
                        if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["component_reference"].parent.properties["name"]')) # from line 27, col 9.
                        write(u'''/''')
                        _v = VFN(VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["component_reference"],"properties",True)["name"] # u'$comp_instance.properties["component_reference"].properties["name"]' on line 27, col 84
                        if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["component_reference"].properties["name"]')) # from line 27, col 84.
                        write(u'''";
\tscheduling_scheme = ''')
                        _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["scheduling_scheme"] # u'$comp_instance.properties["scheduling_scheme"]' on line 28, col 22
                        if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["scheduling_scheme"]')) # from line 28, col 22.
                        write(u''';
\tlogging
\t{
''')
                        if VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["logging_debug"] != False: # generated from line 31, col 1
                            write(u'''\t  DEBUG = true;
''')
                        else: # generated from line 33, col 1
                            write(u'''\t  DEBUG = false;
''')
                        if VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["logging_info"] != False: # generated from line 36, col 1
                            write(u'''\t  INFO = true;
''')
                        else: # generated from line 38, col 1
                            write(u'''\t  INFO = false;
''')
                        if VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["logging_warning"] != False: # generated from line 41, col 1
                            write(u'''\t  WARNING = true;
''')
                        else: # generated from line 43, col 1
                            write(u'''\t  WARNING = false;
''')
                        if VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["logging_error"] != False: # generated from line 46, col 1
                            write(u'''\t  ERROR = true;
''')
                        else: # generated from line 48, col 1
                            write(u'''\t  ERROR = false;
''')
                        if VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["logging_critical"] != False: # generated from line 51, col 1
                            write(u'''\t  CRITICAL = true;
''')
                        else: # generated from line 53, col 1
                            write(u'''\t  CRITICAL = false;
''')
                        write(u'''\t}
      }
''')
                        if VFSL([locals()]+SL+[globals(), builtin],"comp_instance.children",True) != []: # generated from line 58, col 1
                            for port_instance in VFSL([locals()]+SL+[globals(), builtin],"comp_instance.children",True): # generated from line 59, col 1
                                write(u'''      port_instance ''')
                                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"port_instance",True),"properties",True)["name"] # u'$port_instance.properties["name"]' on line 60, col 21
                                if _v is not None: write(_filter(_v, rawExpr=u'$port_instance.properties["name"]')) # from line 60, col 21.
                                write(u''' 
      {
\tref = "''')
                                _v = VFN(VFN(VFN(VFSL([locals()]+SL+[globals(), builtin],"port_instance",True),"properties",True)["port_reference"],"parent",True),"properties",True)["name"] # u'$port_instance.properties["port_reference"].parent.properties["name"]' on line 62, col 9
                                if _v is not None: write(_filter(_v, rawExpr=u'$port_instance.properties["port_reference"].parent.properties["name"]')) # from line 62, col 9.
                                write(u'''/''')
                                _v = VFN(VFN(VFSL([locals()]+SL+[globals(), builtin],"port_instance",True),"properties",True)["port_reference"],"properties",True)["name"] # u'$port_instance.properties["port_reference"].properties["name"]' on line 62, col 79
                                if _v is not None: write(_filter(_v, rawExpr=u'$port_instance.properties["port_reference"].properties["name"]')) # from line 62, col 79.
                                write(u'''";
\tgroup = "''')
                                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"port_instance",True),"properties",True)["group"] # u'$port_instance.properties["group"]' on line 63, col 11
                                if _v is not None: write(_filter(_v, rawExpr=u'$port_instance.properties["group"]')) # from line 63, col 11.
                                write(u'''";
      }
''')
                        write(u'''  }
''')
                write(u'''}
''')
        write(u'''

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

    _mainCheetahMethod_for_rdp= 'respond'

## END CLASS DEFINITION

if not hasattr(rdp, '_initCheetahAttributes'):
    templateAPIClass = getattr(rdp, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(rdp)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=rdp()).run()


