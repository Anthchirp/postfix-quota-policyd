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
    self._level = level

  def info(self, message):
    if self._level >= self.INFO:
      syslog.syslog(syslog.LOG_INFO, message)

  def warn(self, message):
    if self._level >= self.WARN:
      syslog.syslog(syslog.LOG_WARNING, message)

  def debug(self, message):
    if self._level >= self.DEBUG:
      syslog.syslog(syslog.LOG_DEBUG, message)
