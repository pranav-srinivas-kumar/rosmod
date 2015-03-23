/*
 * ROSMOD Logger
 * Author: Pranav Srinivar Kumar
 * Date: 2015.03.21
 */

#include "Logger.hpp"

/*
 * Write remaining log contents to file
 */
Logger::~Logger() {
  if (SIZE_OF_LOG() > 0) {
    WRITE_TO_FILE();
    log_content = "";
  }
  log_stream.close();
}

/*
 * Open file outstream @ provided target path
 */
bool Logger::CREATE_FILE(const char * target_log_path) {
  log_path = target_log_path;
  log_stream.open(log_path, ios::out | ios::app );  
  log_content = "--------------------------------------------------------------------------------";
  return true;
}

/*
 * Write Log contents to file & close stream
 */ 
bool Logger::WRITE_TO_FILE() {
  log_stream << log_content << endl;
  return true;
}

/*
 * Check log content size 
 * If size > 1000, write to file
 */
bool Logger::CHECK_LOG_SIZE() {
  if (SIZE_OF_LOG() > max_log_unit) {
    WRITE_TO_FILE();
    log_content = "";
    return true;
  }
  return false;
}

/*
 * Create a debug log entry
 */
bool Logger::DEBUG(string text) {
  bool exceeded_limit = CHECK_LOG_SIZE();
  if (exceeded_limit == true)
    log_content += "ROSMOD::DEBUG::" + CLOCK_VALUE() + "::" + text;
  else
    log_content += "\nROSMOD::DEBUG::" + CLOCK_VALUE() + "::" + text;
  return true;
}

/*
 * Create an error log entry
 */
bool Logger::ERROR(string text) {
  bool exceeded_limit = CHECK_LOG_SIZE();
  if (exceeded_limit == true)
    log_content += "ROSMOD::ERROR::" + CLOCK_VALUE() + "::" + text;
  else
    log_content += "\nROSMOD::ERROR::" + CLOCK_VALUE() + "::" + text;
  return true;
}

/*
 * Return size of log_content
 */
int Logger::SIZE_OF_LOG() {
  return log_content.size();
}

/*
 * Get Current Clock Value
 */
string Logger::CLOCK_VALUE() {
  stringstream clock_string;
  clock_string << clock.now().time_since_epoch().count();
  return clock_string.str();  
}
