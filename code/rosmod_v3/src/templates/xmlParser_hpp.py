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
__CHEETAH_genTime__ = 1430241675.447761
__CHEETAH_genTimestamp__ = 'Tue Apr 28 12:21:15 2015'
__CHEETAH_src__ = '/home/kelsier/Repositories/rosmod/code/rosmod_v3/src/templates/xmlParser_hpp.tmpl'
__CHEETAH_srcLastModified__ = 'Sun Apr 19 17:15:22 2015'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class xmlParser_hpp(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(xmlParser_hpp, self).__init__(*args, **KWs)
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
        
        write(u'''#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <stdio.h>
#include <map>

#include "boost/filesystem.hpp"

''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 10, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 10, col 1.
        write(u''' "''')
        _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 10, col 16
        if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 10, col 16.
        write(u'''/rapidxml.hpp"
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 11, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 11, col 1.
        write(u''' "''')
        _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 11, col 16
        if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 11, col 16.
        write(u'''/rapidxml_utils.hpp"
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 12, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 12, col 1.
        write(u''' "''')
        _v = VFFSL(SL,"package_name",True) # u'$package_name' on line 12, col 16
        if _v is not None: write(_filter(_v, rawExpr=u'$package_name')) # from line 12, col 16.
        write(u'''/Logger.hpp"
using namespace rapidxml;

class GroupXMLParser
{
public:
  std::map<std::string,std::string> portGroupMap;
  Log_Levels logging;

  void Print()
  {
    std::map<std::string,std::string>::iterator it;
    for (it=portGroupMap.begin(); it!=portGroupMap.end(); ++it)
      std::cout << it->first << " => " << it->second << \'\\n\';
  }

  bool Return_Boolean(std::string value) 
  {
    if (value == "true") 
      return true;
    else
      return false;
  }

  bool Parse(std::string fName)
  {
    if ( !boost::filesystem::exists(fName) )
      return false;
    rapidxml::file<> xmlFile(fName.c_str()); // Default template is char
    rapidxml::xml_document<> doc;
    doc.parse<0>(xmlFile.data());

    /*
     * Establish log levels
     */
    xml_node<> *logger = doc.first_node("logging");
    xml_node<> * debug = logger->first_node("debug");
    
    logging.DEBUG = Return_Boolean(logger->first_node("debug")->first_attribute()->value());
    logging.INFO = Return_Boolean(logger->first_node("info")->first_attribute()->value());
    logging.WARNING = Return_Boolean(logger->first_node("warning")->first_attribute()->value());
    logging.ERROR = Return_Boolean(logger->first_node("error")->first_attribute()->value());
    logging.CRITICAL = Return_Boolean(logger->first_node("critical")->first_attribute()->value());

    for (xml_node<> *node = doc.first_node("group"); node; node = node->next_sibling())
      {
\tstd::string groupID;
\tfor (xml_attribute<> *attr = node->first_attribute();
\t     attr; attr = attr->next_attribute())
\t  {
\t    if ( !strcmp(attr->name(),"ID") )
\t      groupID = attr->value();
\t  }
\tfor (xml_node<> *child = node->first_node("port"); child; child = child->next_sibling())
\t  {
\t    for (xml_attribute<> *attr = child->first_attribute();
\t\t attr; attr = attr->next_attribute())
\t      {
\t\tif ( !strcmp(attr->name(),"ID") )
\t\t    portGroupMap.insert( std::pair<std::string,std::string>(attr->value(),groupID) );
\t      }\t    
\t  }
      }
    return true;
  }
};
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

    _mainCheetahMethod_for_xmlParser_hpp= 'respond'

## END CLASS DEFINITION

if not hasattr(xmlParser_hpp, '_initCheetahAttributes'):
    templateAPIClass = getattr(xmlParser_hpp, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(xmlParser_hpp)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=xmlParser_hpp()).run()


