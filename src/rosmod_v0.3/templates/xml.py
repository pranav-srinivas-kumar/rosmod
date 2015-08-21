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
__CHEETAH_genTime__ = 1440180609.100208
__CHEETAH_genTimestamp__ = 'Fri Aug 21 13:10:09 2015'
__CHEETAH_src__ = '/home/jeb/Repositories/rosmod-gui/src/rosmod_v0.3/templates/xml.tmpl'
__CHEETAH_srcLastModified__ = 'Sat Jul 11 17:49:35 2015'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class xml(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(xml, self).__init__(*args, **KWs)
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
        
        write(u'''<?xml version="1.0"?>
<node name="''')
        _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"node",True),"properties",True)["name"] # u'$node.properties["name"]' on line 2, col 13
        if _v is not None: write(_filter(_v, rawExpr=u'$node.properties["name"]')) # from line 2, col 13.
        write(u'''">
''')
        if VFSL([locals()]+SL+[globals(), builtin],"node.children",True) != []: # generated from line 3, col 1
            if VFSL([locals()]+SL+[globals(), builtin],"needs_io",True): # generated from line 4, col 1
                write(u'''  <library name="libKRPCI.so"/>
''')
            for comp_instance in VFSL([locals()]+SL+[globals(), builtin],"node.children",True): # generated from line 7, col 1
                write(u'''  <component_instance name="''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["name"] # u'$comp_instance.properties["name"]' on line 8, col 29
                if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["name"]')) # from line 8, col 29.
                write(u'''">
    <library name="lib''')
                _v = VFN(VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["component_reference"],"properties",True)["name"] # u'${comp_instance.properties["component_reference"].properties["name"]}' on line 9, col 23
                if _v is not None: write(_filter(_v, rawExpr=u'${comp_instance.properties["component_reference"].properties["name"]}')) # from line 9, col 23.
                write(u'''.so"/>
    <scheduling_scheme setting="''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["scheduling_scheme"] # u'$comp_instance.properties["scheduling_scheme"]' on line 10, col 33
                if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["scheduling_scheme"]')) # from line 10, col 33.
                write(u'''"/>
    <logging>
      <debug setting="''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["logging_debug"] # u'$comp_instance.properties["logging_debug"]' on line 12, col 23
                if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["logging_debug"]')) # from line 12, col 23.
                write(u'''"/>
      <info setting="''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["logging_info"] # u'$comp_instance.properties["logging_info"]' on line 13, col 22
                if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["logging_info"]')) # from line 13, col 22.
                write(u'''"/>
      <warning setting="''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["logging_warning"] # u'$comp_instance.properties["logging_warning"]' on line 14, col 25
                if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["logging_warning"]')) # from line 14, col 25.
                write(u'''"/>
      <error setting="''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["logging_error"] # u'$comp_instance.properties["logging_error"]' on line 15, col 23
                if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["logging_error"]')) # from line 15, col 23.
                write(u'''"/>
      <critical setting="''')
                _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"comp_instance",True),"properties",True)["logging_critical"] # u'$comp_instance.properties["logging_critical"]' on line 16, col 26
                if _v is not None: write(_filter(_v, rawExpr=u'$comp_instance.properties["logging_critical"]')) # from line 16, col 26.
                write(u'''"/>
    </logging>
''')
                if VFSL([locals()]+SL+[globals(), builtin],"comp_instance.children",True) != []: # generated from line 18, col 1
                    for port_instance in VFSL([locals()]+SL+[globals(), builtin],"comp_instance.children",True): # generated from line 19, col 1
                        write(u'''    <port_instance name="''')
                        _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"port_instance",True),"properties",True)["name"] # u'$port_instance.properties["name"]' on line 20, col 26
                        if _v is not None: write(_filter(_v, rawExpr=u'$port_instance.properties["name"]')) # from line 20, col 26.
                        write(u'''">
      <port name="''')
                        _v = VFN(VFN(VFSL([locals()]+SL+[globals(), builtin],"port_instance",True),"properties",True)["port_reference"],"properties",True)["name"] # u'$port_instance.properties["port_reference"].properties["name"]' on line 21, col 19
                        if _v is not None: write(_filter(_v, rawExpr=u'$port_instance.properties["port_reference"].properties["name"]')) # from line 21, col 19.
                        write(u'''"/>
      <group setting="''')
                        _v = VFN(VFSL([locals()]+SL+[globals(), builtin],"port_instance",True),"properties",True)["group"] # u'$port_instance.properties["group"]' on line 22, col 23
                        if _v is not None: write(_filter(_v, rawExpr=u'$port_instance.properties["group"]')) # from line 22, col 23.
                        write(u'''"/>
    </port_instance>
''')
                write(u'''  </component_instance>
''')
        write(u'''</node>

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

    _mainCheetahMethod_for_xml= 'respond'

## END CLASS DEFINITION

if not hasattr(xml, '_initCheetahAttributes'):
    templateAPIClass = getattr(xml, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(xml)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=xml()).run()


