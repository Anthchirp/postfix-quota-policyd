import MySQLdb

class _mysql_connection():
  def __init__(self):
    # Set some sensible defaults
    self._db_host = '127.0.0.1'
    self._db_user = 'quotapolicyd'
    self._db_pass = 'quotapolicyd'
    self._db_db   = 'quotapolicyd'

    self._connected = False

  def connect(self):
    self._connected = True

  def is_connected(self):
    return self._connected

  def _set_parameter(self, option, opt, value, parser):
    print [option, opt, value, parser]

  def add_command_line_options(self, optparser):
    optparser.add_option('--db-host', metavar='HOST',
      default=self._db_host,
      help='MySQL host address, default %default',
      type='string', nargs=1, dest='db-host',
      action='callback', callback=self._set_parameter)

connection = _mysql_connection()
