import mock
import optparse
from quotapolicyd.log import Logger

@mock.patch('quotapolicyd.log.syslog')
def test_parse_command_line_options(sysmock):
  '''Adding '-v' to command line should enable debug logging.'''
  parser = optparse.OptionParser()

  log = Logger()
  log.debug('')
  assert not sysmock.syslog.called

  log.add_command_line_options(parser)
  parser.parse_args(['-v'])
  log.debug('')
  assert sysmock.syslog.called

@mock.patch('quotapolicyd.log.syslog')
def test_write_to_syslog(sysmock):
  '''Check that messages are passed on to syslog with appropriate flags set.'''
  sysmock.LOG_PID = mock.sentinel.PID
  sysmock.LOG_MAIL = mock.sentinel.MAIL
  sysmock.LOG_INFO = mock.sentinel.INFO
  sysmock.LOG_WARNING = mock.sentinel.WARN
  sysmock.LOG_DEBUG = mock.sentinel.DEBUG

  messages = { lvl: '{0}message'.format(lvl)
      for lvl in ['debug', 'warn', 'info'] }

  log = Logger()
  log.set_log_level(log.DEBUG)
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

@mock.patch('quotapolicyd.log.syslog')
def test_syslog_log_levels(sysmock):
  '''Check log levels and filters.'''
  log = Logger()

  # implied default level: log.INFO
  log.debug('')
  log.info('')
  log.warn('')
  assert sysmock.syslog.call_count == 2

  log.set_log_level(log.DEBUG)
  log.debug('')
  log.info('')
  log.warn('')
  assert sysmock.syslog.call_count == 2 + 3

  log.set_log_level(log.INFO)
  log.debug('')
  log.info('')
  log.warn('')
  assert sysmock.syslog.call_count == 2 + 3 + 2

  log.set_log_level(log.WARN)
  log.debug('')
  log.info('')
  log.warn('')
  assert sysmock.syslog.call_count == 2 + 3 + 2 + 1
