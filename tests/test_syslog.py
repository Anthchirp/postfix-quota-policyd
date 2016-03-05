import mock
from quotapolicyd.log import Logger

@mock.patch('quotapolicyd.log.syslog')
def test_write_to_syslog(sysmock):
  log = Logger()

  messages = { lvl: '%smessage' % lvl
      for lvl in ['debug', 'warn', 'info'] }

  log.info(messages['info'])
  log.warn(messages['warn'])
  log.debug(messages['debug'])

  del log

  assert sysmock.openlog.call_count == 1
  assert sysmock.syslog.call_count == 3

  try:
    import gc
    gc.collect()
    assert sysmock.closelog.call_count == 1
  except ImportError:
    print "Garbage collection test skipped"
#
#import syslog
#
#syslog.syslog('Processing started')
#if error:
#    syslog.syslog(syslog.LOG_ERR, 'Processing started')
#
#An example of setting some log options, these would include the process ID in logged messages, and write the messages to the destination facility used for mail logging:
#
#s#yslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)
#sy#slog.syslog('E-mail processing initiated...')
#
