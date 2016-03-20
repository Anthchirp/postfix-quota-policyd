import syslog

class Logger():
  def __init__(self):
    syslog.openlog(
      ident="quotapolicyd",
      logoption=syslog.LOG_PID,
      facility=syslog.LOG_MAIL
    )

    self.WARN = 0
    self.INFO = 1
    self.DEBUG = 2
    self._level = self.INFO

  def set_log_level(self, level):
    '''Set a defined logging level and filter all messages below the threshold.'''
    self._level = level

  def info(self, message):
    '''log message, info level (medium)'''
    if self._level >= self.INFO:
      syslog.syslog(syslog.LOG_INFO, message)

  def warn(self, message):
    '''log message, warning level (highest)'''
    if self._level >= self.WARN:
      syslog.syslog(syslog.LOG_WARNING, message)

  def debug(self, message):
    '''log message, debug level (lowest)'''
    if self._level >= self.DEBUG:
      syslog.syslog(syslog.LOG_DEBUG, message)

  def _set_parameter(self, option, opt, value, parser):
    '''callback function for optionparser'''
    del option, parser, value # unused
    if opt == '-v':
      self.set_log_level(self.DEBUG)

  def add_command_line_options(self, optparser):
    '''function to inject command line parameters'''
    optparser.add_option('-v', '--verbose',
      help='increate logging verbosity',
      action='callback', callback=self._set_parameter)
