import mock
from quotapolicyd.log import Logger

@mock.patch('quotapolicyd.log.syslog')
def test_write_to_syslog(sysmock):
  sysmock.LOG_PID = mock.sentinel.PID
  sysmock.LOG_MAIL = mock.sentinel.MAIL
  sysmock.LOG_INFO = mock.sentinel.INFO
  sysmock.LOG_WARNING = mock.sentinel.WARN
  sysmock.LOG_DEBUG = mock.sentinel.DEBUG

  messages = { lvl: '%smessage' % lvl
      for lvl in ['debug', 'warn', 'info'] }

  log = Logger()
  log.info(messages['info'])
  assert sysmock.syslog.call_count == 1
  assert sysmock.syslog.call_args == ((mock.sentinel.INFO, mock.ANY), {})
  assert messages['info'] in sysmock.syslog.call_args[0][1]

  log.warn(messages['warn'])
  assert sysmock.syslog.call_count == 2
  assert sysmock.syslog.call_args == ((mock.sentinel.WARN, mock.ANY), {})
  assert messages['warn'] in sysmock.syslog.call_args[0][1]

  log.debug(messages['debug'])
  assert sysmock.syslog.call_count == 3
  assert sysmock.syslog.call_args == ((mock.sentinel.DEBUG, mock.ANY), {})
  assert messages['debug'] in sysmock.syslog.call_args[0][1]

  assert sysmock.openlog.call_count == 1
  args, kwargs = sysmock.openlog.call_args
  assert args == ()
  assert kwargs == {
      'ident': 'quotapolicyd',
      'facility': mock.sentinel.MAIL,
      'logoption': mock.sentinel.PID
    }
