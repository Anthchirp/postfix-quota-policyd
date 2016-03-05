import syslog

class Logger():
  def __init__(self):
    self.connected = False
    syslog.openlog(
      ident="quotapolicyd",
      logoption=syslog.LOG_PID,
      facility=syslog.LOG_MAIL
    )

  def __del__(self):
    syslog.closelog()

  def info(self, message):
    syslog.syslog(syslog.LOG_INFO, message)

  def warn(self, message):
    syslog.syslog(syslog.LOG_WARNING, message)

  def debug(self, message):
    syslog.syslog(syslog.LOG_DEBUG, message)
