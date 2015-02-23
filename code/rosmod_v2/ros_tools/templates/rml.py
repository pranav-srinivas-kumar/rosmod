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
__CHEETAH_genTime__ = 1424717485.577047
__CHEETAH_genTimestamp__ = 'Mon Feb 23 12:51:25 2015'
__CHEETAH_src__ = '/home/jeb/Repositories/rosmod/code/rosmod_v2/ros_tools/templates/rml.tmpl'
__CHEETAH_srcLastModified__ = 'Mon Feb 23 12:11:13 2015'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class rml(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(rml, self).__init__(*args, **KWs)
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
        
        write(u'''workspace ''')
        _v = VFN(VFFSL(SL,"workspace",True),"properties",True)["name"] # u'$workspace.properties["name"]' on line 1, col 11
        if _v is not None: write(_filter(_v, rawExpr=u'$workspace.properties["name"]')) # from line 1, col 11.
        write(u'''

''')
        if VFFSL(SL,"workspace.children",True) != []: # generated from line 3, col 1
            for package in VFFSL(SL,"workspace.children",True): # generated from line 4, col 1
                write(u'''package ''')
                _v = VFN(VFFSL(SL,"package",True),"properties",True)["name"] # u'$package.properties["name"]' on line 5, col 9
                if _v is not None: write(_filter(_v, rawExpr=u'$package.properties["name"]')) # from line 5, col 9.
                write(u'''
{
''')
                if VFN(VFFSL(SL,"package",True),"getChildrenByKind",False)("message") != []: # generated from line 7, col 1
                    write(u'''    // Set of ROS Messages
    messages 
    {
''')
                    for message in VFN(VFFSL(SL,"package",True),"getChildrenByKind",False)("message"): # generated from line 11, col 1
                        write(u'''        // ROS msg - ''')
                        _v = VFN(VFFSL(SL,"message",True),"properties",True)["name"] # u'$message.properties["name"]' on line 12, col 22
                        if _v is not None: write(_filter(_v, rawExpr=u'$message.properties["name"]')) # from line 12, col 22.
                        write(u'''
        msg ''')
                        _v = VFN(VFFSL(SL,"message",True),"properties",True)["name"] # u'$message.properties["name"]' on line 13, col 13
                        if _v is not None: write(_filter(_v, rawExpr=u'$message.properties["name"]')) # from line 13, col 13.
                        write(u'''
        {
''')
                        for field in VFN(VFFSL(SL,"message",True),"properties",True)["fields"]            : # generated from line 15, col 1
                            if VFFSL(SL,"len",False)(field) > 2: # generated from line 16, col 1
                                write(u'''            ''')
                                _v = VFFSL(SL,"field",True)[0] # u'$field[0]' on line 17, col 13
                                if _v is not None: write(_filter(_v, rawExpr=u'$field[0]')) # from line 17, col 13.
                                write(u''' ''')
                                _v = VFFSL(SL,"field",True)[1] # u'$field[1]' on line 17, col 23
                                if _v is not None: write(_filter(_v, rawExpr=u'$field[1]')) # from line 17, col 23.
                                write(u'''=''')
                                _v = VFFSL(SL,"field",True)[2] # u'$field[2]' on line 17, col 33
                                if _v is not None: write(_filter(_v, rawExpr=u'$field[2]')) # from line 17, col 33.
                                write(u''';
''')
                            else: # generated from line 18, col 1
                                write(u'''            ''')
                                _v = VFFSL(SL,"field",True)[0] # u'$field[0]' on line 19, col 13
                                if _v is not None: write(_filter(_v, rawExpr=u'$field[0]')) # from line 19, col 13.
                                write(u''' ''')
                                _v = VFFSL(SL,"field",True)[1] # u'$field[1]' on line 19, col 23
                                if _v is not None: write(_filter(_v, rawExpr=u'$field[1]')) # from line 19, col 23.
                                write(u''';
''')
                        write(u'''        } 
''')
                    write(u'''    }
''')
                write(u'''
''')
                if VFN(VFFSL(SL,"package",True),"getChildrenByKind",False)("service") != []: # generated from line 27, col 1
                    write(u'''    // Set of ROS Services
    services
    {
''')
                    for service in VFN(VFFSL(SL,"package",True),"getChildrenByKind",False)("service"): # generated from line 31, col 1
                        write(u'''        // ROS srv - ''')
                        _v = VFN(VFFSL(SL,"service",True),"properties",True)["name"] # u'$service.properties["name"]' on line 32, col 22
                        if _v is not None: write(_filter(_v, rawExpr=u'$service.properties["name"]')) # from line 32, col 22.
                        write(u'''
        srv ''')
                        _v = VFN(VFFSL(SL,"service",True),"properties",True)["name"] # u'$service.properties["name"]' on line 33, col 13
                        if _v is not None: write(_filter(_v, rawExpr=u'$service.properties["name"]')) # from line 33, col 13.
                        write(u'''
        {
            request
            {
''')
                        for req_field in VFN(VFFSL(SL,"service",True),"properties",True)["request"]: # generated from line 37, col 1
                            if VFFSL(SL,"len",False)(req_field) > 2: # generated from line 38, col 1
                                write(u'''                ''')
                                _v = VFFSL(SL,"req_field",True)[0] # u'$req_field[0]' on line 39, col 17
                                if _v is not None: write(_filter(_v, rawExpr=u'$req_field[0]')) # from line 39, col 17.
                                write(u''' ''')
                                _v = VFFSL(SL,"req_field",True)[1] # u'$req_field[1]' on line 39, col 31
                                if _v is not None: write(_filter(_v, rawExpr=u'$req_field[1]')) # from line 39, col 31.
                                write(u'''=''')
                                _v = VFFSL(SL,"req_field",True)[2] # u'$req_field[2]' on line 39, col 45
                                if _v is not None: write(_filter(_v, rawExpr=u'$req_field[2]')) # from line 39, col 45.
                                write(u''';
''')
                            else: # generated from line 40, col 1
                                write(u'''                ''')
                                _v = VFFSL(SL,"req_field",True)[0] # u'$req_field[0]' on line 41, col 17
                                if _v is not None: write(_filter(_v, rawExpr=u'$req_field[0]')) # from line 41, col 17.
                                write(u''' ''')
                                _v = VFFSL(SL,"req_field",True)[1] # u'$req_field[1]' on line 41, col 31
                                if _v is not None: write(_filter(_v, rawExpr=u'$req_field[1]')) # from line 41, col 31.
                                write(u''';
''')
                        write(u'''            }

            response
            {
''')
                        for res_field in VFN(VFFSL(SL,"service",True),"properties",True)["response"]: # generated from line 48, col 1
                            if VFFSL(SL,"len",False)(res_field) > 2: # generated from line 49, col 1
                                write(u'''                ''')
                                _v = VFFSL(SL,"res_field",True)[0] # u'$res_field[0]' on line 50, col 17
                                if _v is not None: write(_filter(_v, rawExpr=u'$res_field[0]')) # from line 50, col 17.
                                write(u''' ''')
                                _v = VFFSL(SL,"res_field",True)[1] # u'$res_field[1]' on line 50, col 31
                                if _v is not None: write(_filter(_v, rawExpr=u'$res_field[1]')) # from line 50, col 31.
                                write(u'''=''')
                                _v = VFFSL(SL,"res_field",True)[2] # u'$res_field[2]' on line 50, col 45
                                if _v is not None: write(_filter(_v, rawExpr=u'$res_field[2]')) # from line 50, col 45.
                                write(u''';
''')
                            else: # generated from line 51, col 1
                                write(u'''                ''')
                                _v = VFFSL(SL,"res_field",True)[0] # u'$res_field[0]' on line 52, col 17
                                if _v is not None: write(_filter(_v, rawExpr=u'$res_field[0]')) # from line 52, col 17.
                                write(u''' ''')
                                _v = VFFSL(SL,"res_field",True)[1] # u'$res_field[1]' on line 52, col 31
                                if _v is not None: write(_filter(_v, rawExpr=u'$res_field[1]')) # from line 52, col 31.
                                write(u''';
''')
                        write(u'''            }
        }
''')
                    write(u'''    }
''')
                write(u'''
''')
                if VFN(VFFSL(SL,"package",True),"getChildrenByKind",False)("component") != []: # generated from line 61, col 1
                    write(u'''    // Set of ROS Components
    components
    {
''')
                    for component in VFN(VFFSL(SL,"package",True),"getChildrenByKind",False)("component"): # generated from line 65, col 1
                        write(u'''        // ROS Component - ''')
                        _v = VFN(VFFSL(SL,"component",True),"properties",True)["name"] # u'$component.properties["name"]' on line 66, col 28
                        if _v is not None: write(_filter(_v, rawExpr=u'$component.properties["name"]')) # from line 66, col 28.
                        write(u'''
\tcomponent
\t{
''')
                        if VFN(VFFSL(SL,"component",True),"getChildrenByKind",False)("server") != []: # generated from line 69, col 1
                            for server in VFN(VFFSL(SL,"component",True),"getChildrenByKind",False)("server"): # generated from line 70, col 1
                                write(u'''            provides ''')
                                _v = VFN(VFN(VFFSL(SL,"server",True),"properties",True)["service_reference"],"properties",True)["name"] # u'$server.properties["service_reference"].properties["name"]' on line 71, col 22
                                if _v is not None: write(_filter(_v, rawExpr=u'$server.properties["service_reference"].properties["name"]')) # from line 71, col 22.
                                write(u''';
''')
                        write(u'''
''')
                        if VFN(VFFSL(SL,"component",True),"getChildrenByKind",False)("client") != []: # generated from line 75, col 1
                            for client in VFN(VFFSL(SL,"component",True),"getChildrenByKind",False)("client"): # generated from line 76, col 1
                                write(u'''\t    requires ''')
                                _v = VFN(VFN(VFFSL(SL,"client",True),"properties",True)["service_reference"],"properties",True)["name"] # u'$client.properties["service_reference"].properties["name"]' on line 77, col 15
                                if _v is not None: write(_filter(_v, rawExpr=u'$client.properties["service_reference"].properties["name"]')) # from line 77, col 15.
                                write(u''';
''')
                        write(u'''
''')
                        if VFN(VFFSL(SL,"component",True),"getChildrenByKind",False)("publisher") != []: # generated from line 81, col 1
                            for pb in VFN(VFFSL(SL,"component",True),"getChildrenByKind",False)("publisher"): # generated from line 82, col 1
                                write(u'''\t    publisher<''')
                                _v = VFN(VFN(VFFSL(SL,"pb",True),"properties",True)["message_reference"],"properties",True)["name"] # u'$pb.properties["message_reference"].properties["name"]' on line 83, col 16
                                if _v is not None: write(_filter(_v, rawExpr=u'$pb.properties["message_reference"].properties["name"]')) # from line 83, col 16.
                                write(u'''> ''')
                                _v = VFN(VFFSL(SL,"pb",True),"properties",True)["name"] # u'$pb.properties["name"]' on line 83, col 72
                                if _v is not None: write(_filter(_v, rawExpr=u'$pb.properties["name"]')) # from line 83, col 72.
                                write(u''';     
''')
                        write(u'''
''')
                        if VFN(VFFSL(SL,"component",True),"getChildrenByKind",False)("subscriber") != []: # generated from line 87, col 1
                            for sb in VFN(VFFSL(SL,"component",True),"getChildrenByKind",False)("subscriber"): # generated from line 88, col 1
                                write(u'''     \t    subscriber<''')
                                _v = VFN(VFN(VFFSL(SL,"sb",True),"properties",True)["message_reference"],"properties",True)["name"] # u'$sb.properties["message_reference"].properties["name"]' on line 89, col 22
                                if _v is not None: write(_filter(_v, rawExpr=u'$sb.properties["message_reference"].properties["name"]')) # from line 89, col 22.
                                write(u'''> ''')
                                _v = VFN(VFFSL(SL,"sb",True),"properties",True)["name"] # u'$sb.properties["name"]' on line 89, col 78
                                if _v is not None: write(_filter(_v, rawExpr=u'$sb.properties["name"]')) # from line 89, col 78.
                                write(u''';
''')
                        write(u'''
''')
                        if VFN(VFFSL(SL,"component",True),"getChildrenByKind",False)("timer") != []: # generated from line 93, col 1
                            for timer in VFN(VFFSL(SL,"component",True),"getChildrenByKind",False)("timer"): # generated from line 94, col 1
                                write(u'''\t    timer ''')
                                _v = VFN(VFFSL(SL,"timer",True),"properties",True)["name"] # u'$timer.properties["name"]' on line 95, col 12
                                if _v is not None: write(_filter(_v, rawExpr=u'$timer.properties["name"]')) # from line 95, col 12.
                                write(u'''
\t    {
\t        period = ''')
                                _v = VFN(VFFSL(SL,"timer",True),"properties",True)["period"] # u'$timer.properties["period"]' on line 97, col 19
                                if _v is not None: write(_filter(_v, rawExpr=u'$timer.properties["period"]')) # from line 97, col 19.
                                _v = VFN(VFFSL(SL,"timer",True),"properties",True)["unit"] # u'$timer.properties["unit"]' on line 97, col 46
                                if _v is not None: write(_filter(_v, rawExpr=u'$timer.properties["unit"]')) # from line 97, col 46.
                                write(u''';
\t    }
''')
                        write(u'''\t}
''')
                    write(u'''    }
''')
                write(u'''
''')
                if VFN(VFFSL(SL,"package",True),"getChildrenByKind",False)("node") != []: # generated from line 106, col 1
                    write(u'''    // Set of ROS Nodes in this package
    nodes
    {
''')
                    for node in VFN(VFFSL(SL,"package",True),"getChildrenByKind",False)("node"): # generated from line 110, col 1
                        write(u'''        node ''')
                        _v = VFN(VFFSL(SL,"node",True),"properties",True)["name"] # u'$node.properties["name"]' on line 111, col 14
                        if _v is not None: write(_filter(_v, rawExpr=u'$node.properties["name"]')) # from line 111, col 14.
                        write(u''' 
\t{
''')
                        if VFN(VFFSL(SL,"node",True),"getChildrenByKind",False)("component_instance") != []: # generated from line 113, col 1
                            write(u'''            // Instantiating components in ROS node
''')
                            for instance in VFN(VFFSL(SL,"node",True),"getChildrenByKind",False)("component_instance"): # generated from line 115, col 1
                                write(u'''     \t    component<''')
                                _v = VFN(VFN(VFFSL(SL,"instance",True),"properties",True)["component_reference"],"properties",True)["name"] # u'$instance.properties["component_reference"].properties["name"]' on line 116, col 21
                                if _v is not None: write(_filter(_v, rawExpr=u'$instance.properties["component_reference"].properties["name"]')) # from line 116, col 21.
                                write(u'''> ''')
                                _v = VFN(VFFSL(SL,"instance",True),"properties",True)["name"] # u'$instance.properties["name"]' on line 116, col 85
                                if _v is not None: write(_filter(_v, rawExpr=u'$instance.properties["name"]')) # from line 116, col 85.
                                write(u''';
''')
                        write(u'''\t}
''')
                    write(u'''    }
''')
                write(u'''}
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

    _mainCheetahMethod_for_rml= 'respond'

## END CLASS DEFINITION

if not hasattr(rml, '_initCheetahAttributes'):
    templateAPIClass = getattr(rml, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(rml)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=rml()).run()


