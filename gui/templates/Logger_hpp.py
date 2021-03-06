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
__CHEETAH_genTime__ = 1458422848.720611
__CHEETAH_genTimestamp__ = 'Sat Mar 19 16:27:28 2016'
__CHEETAH_src__ = '/home/jeb/Repositories/rosmod/gui/templates/Logger_hpp.tmpl'
__CHEETAH_srcLastModified__ = 'Tue Mar  8 10:57:08 2016'
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
''')
        _v = VFFSL(SL,"hash_include",True) # u'$hash_include' on line 10, col 1
        if _v is not None: write(_filter(_v, rawExpr=u'$hash_include')) # from line 10, col 1.
        write(u''' <typeinfo>

class Logger 
{

public:

  Logger() {
    logs_to_file_ = false;
    is_periodic_ = true;
    max_log_unit_ = 1;
    log_content_ = "=================================================================\\n";
  }

  void set_is_periodic(bool is_periodic) {
    is_periodic_ = is_periodic;
  }

  void set_max_log_unit(int max_log_unit) {
    max_log_unit_ = max_log_unit;
  }

  void set_logs_to_file(bool logs_to_file) {
    logs_to_file_ = logs_to_file;
  }

  ~Logger() {
    write();
    log_stream_.close();
  }

  bool create_file(std::string log_path) {
    log_path_ = log_path;
    log_stream_.open(log_path_, std::ios::out | std::ios::app);
    logs_to_file_ = true;
    return true;
  }
  
  bool write() {
    if (logs_to_file_) {
      log_stream_ << log_content_;
      log_stream_.flush();
    }
    else
      printf("%s", log_content_.c_str());
    return true;
  }

  bool flush() {
    if (is_periodic_ && size() > max_log_unit_) {
      write();
      log_content_ = "";
      return true;
    }
    return false;
  }

  bool log(std::string log_level, const char * format, ...) {
      va_list args;
      va_start (args, format);
      char log_entry[1024];
      vsprintf (log_entry, format, args);
      std::string log_entry_string(log_entry);
      va_end (args);
      log_content_ += "ROSMOD::" + log_level  + "::" + clock() + 
\t"::" + log_entry_string + "\\n";
      flush();
  }

  int size() {
    return log_content_.size();
  }

  std::string clock() {
    std::stringstream clock_string;
    clock_string << clock_.now().time_since_epoch().count();
    return clock_string.str();
  }

private:
  std::ofstream log_stream_;
  std::string log_content_;
  std::string log_path_;
  bool is_periodic_;
  bool logs_to_file_;
  int max_log_unit_;
  std::chrono::high_resolution_clock clock_;
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


