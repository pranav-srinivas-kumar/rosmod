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
__CHEETAH_genTime__ = 1438799995.399798
__CHEETAH_genTimestamp__ = 'Wed Aug  5 13:39:55 2015'
__CHEETAH_src__ = '/home/jeb/Repositores/rosmod-gui/src/rosmod_v0.3/templates/Logger_hpp.tmpl'
__CHEETAH_srcLastModified__ = 'Mon Jul 13 11:36:12 2015'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class Logger_hpp(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(Logger_hpp, self).__init__(*args, **KWs)
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
        
        write(u'''#ifndef LOGGER_HPP
#define LOGGER_HPP

''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 4, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 4, col 1.
        write(u''' <iostream>
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 5, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 5, col 1.
        write(u''' <stdarg.h>
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 6, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 6, col 1.
        write(u''' <fstream>
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 7, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 7, col 1.
        write(u''' <string>
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 8, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 8, col 1.
        write(u''' <sstream>
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 9, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 9, col 1.
        write(u''' <chrono>

using namespace std;

/*
 * Log Levels in ROSMOD
 * DEBUG: 
 */
struct Log_Levels {
  bool DEBUG;
  bool INFO;
  bool WARNING;
  bool ERROR;
  bool CRITICAL;

  Log_Levels()
  {
    DEBUG = false;
    INFO = true;
    WARNING = false;
    ERROR = true;
    CRITICAL = true;
  }
};

/*
 * Logger class
 * An object of this class is part of every Component instance
 */
class Logger 
{

public:

  // Writes log_content to log file & empties log_content
  ~Logger();

  // Create log file
  bool CREATE_FILE(string target_log_path);

  // Write log contents to file
  bool WRITE_TO_FILE();

  // Check size of log_contents
  bool CHECK_LOG_SIZE();

  // Create a DEBUG log entry
  bool DEBUG(const char * format, ...);

  // Create a INFO log entry
  bool INFO(const char * format, ...);

  // Create a WARNINGg log entry
  bool WARNING(const char * format, ...);

  // Create an ERROR log entry
  bool ERROR(const char * format, ...);

  // Create a CRITICAL log entry
  bool CRITICAL(const char * format, ...);

  // Set Log Levels
  bool SET_LOG_LEVELS(Log_Levels target_log_levels);

  // Get log entry size
  int SIZE_OF_LOG();

  // Get Current Clock Value
  string CLOCK_VALUE();

private:
  // String representing the contents of log
  string log_content;

  // Max size of log_content before contents are written to file
  const int max_log_unit = 1000;

  // Log file stream
  ofstream log_stream;

  // Absolute path of log file
  string log_path;

  // Level of Logging
  Log_Levels log_levels;

  // High Resolution Clock
  chrono::high_resolution_clock clock;
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

    _mainCheetahMethod_for_Logger_hpp= 'respond'

## END CLASS DEFINITION

if not hasattr(Logger_hpp, '_initCheetahAttributes'):
    templateAPIClass = getattr(Logger_hpp, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(Logger_hpp)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=Logger_hpp()).run()


