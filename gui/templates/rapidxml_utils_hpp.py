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
__CHEETAH_genTime__ = 1458422848.980832
__CHEETAH_genTimestamp__ = 'Sat Mar 19 16:27:28 2016'
__CHEETAH_src__ = '/home/jeb/Repositories/rosmod/gui/templates/rapidxml_utils_hpp.tmpl'
__CHEETAH_srcLastModified__ = 'Tue Mar  8 10:57:08 2016'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class rapidxml_utils_hpp(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(rapidxml_utils_hpp, self).__init__(*args, **KWs)
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
        
        write(u'''#ifndef RAPIDXML_UTILS_HPP_INCLUDED\r
#define RAPIDXML_UTILS_HPP_INCLUDED\r
\r
// Copyright (C) 2006, 2009 Marcin Kalicinski\r
// Version 1.13\r
// Revision $DateTime: 2009/05/13 01:46:17 $\r
//! \\file rapidxml_utils.hpp This file contains high-level rapidxml utilities that can be useful\r
//! in certain simple scenarios. They should probably not be used if maximizing performance is the main objective.\r
\r
#include "rapidxml.hpp"\r
#include <vector>\r
#include <string>\r
#include <fstream>\r
#include <stdexcept>\r
\r
namespace rapidxml\r
{\r
\r
    //! Represents data loaded from a file\r
    template<class Ch = char>\r
    class file\r
    {\r
        \r
    public:\r
        \r
        //! Loads file into the memory. Data will be automatically destroyed by the destructor.\r
        //! \\param filename Filename to load.\r
        file(const char *filename)\r
        {\r
            using namespace std;\r
\r
            // Open stream\r
            basic_ifstream<Ch> stream(filename, ios::binary);\r
            if (!stream)\r
                throw runtime_error(string("cannot open file ") + filename);\r
            stream.unsetf(ios::skipws);\r
            \r
            // Determine stream size\r
            stream.seekg(0, ios::end);\r
            size_t size = stream.tellg();\r
            stream.seekg(0);   \r
            \r
            // Load data and add terminating 0\r
            m_data.resize(size + 1);\r
            stream.read(&m_data.front(), static_cast<streamsize>(size));\r
            m_data[size] = 0;\r
        }\r
\r
        //! Loads file into the memory. Data will be automatically destroyed by the destructor\r
        //! \\param stream Stream to load from\r
        file(std::basic_istream<Ch> &stream)\r
        {\r
            using namespace std;\r
\r
            // Load data and add terminating 0\r
            stream.unsetf(ios::skipws);\r
            m_data.assign(istreambuf_iterator<Ch>(stream), istreambuf_iterator<Ch>());\r
            if (stream.fail() || stream.bad())\r
                throw runtime_error("error reading stream");\r
            m_data.push_back(0);\r
        }\r
        \r
        //! Gets file data.\r
        //! \\return Pointer to data of file.\r
        Ch *data()\r
        {\r
            return &m_data.front();\r
        }\r
\r
        //! Gets file data.\r
        //! \\return Pointer to data of file.\r
        const Ch *data() const\r
        {\r
            return &m_data.front();\r
        }\r
\r
        //! Gets file data size.\r
        //! \\return Size of file data, in characters.\r
        std::size_t size() const\r
        {\r
            return m_data.size();\r
        }\r
\r
    private:\r
\r
        std::vector<Ch> m_data;   // File data\r
\r
    };\r
\r
    //! Counts children of node. Time complexity is O(n).\r
    //! \\return Number of children of node\r
    template<class Ch>\r
    inline std::size_t count_children(xml_node<Ch> *node)\r
    {\r
        xml_node<Ch> *child = node->first_node();\r
        std::size_t count = 0;\r
        while (child)\r
        {\r
            ++count;\r
            child = child->next_sibling();\r
        }\r
        return count;\r
    }\r
\r
    //! Counts attributes of node. Time complexity is O(n).\r
    //! \\return Number of attributes of node\r
    template<class Ch>\r
    inline std::size_t count_attributes(xml_node<Ch> *node)\r
    {\r
        xml_attribute<Ch> *attr = node->first_attribute();\r
        std::size_t count = 0;\r
        while (attr)\r
        {\r
            ++count;\r
            attr = attr->next_attribute();\r
        }\r
        return count;\r
    }\r
\r
}\r
\r
#endif\r
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

    _mainCheetahMethod_for_rapidxml_utils_hpp= 'respond'

## END CLASS DEFINITION

if not hasattr(rapidxml_utils_hpp, '_initCheetahAttributes'):
    templateAPIClass = getattr(rapidxml_utils_hpp, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(rapidxml_utils_hpp)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=rapidxml_utils_hpp()).run()


