import MySQLdb

class db_link():
  def __init__(self):
    # Set some sensible defaults
    self._db_host = '127.0.0.1'
    self._db_port = '3306'
    self._db_user = 'quotapolicyd'
    self._db_pass = 'quotapolicyd'
    self._db_db   = 'quotapolicyd'

    self._connected = False
    self._db = None

  def connect(self):
    if self._connected: return
    self._db = MySQLdb.connect(
      host = self._db_host,
      port = self._db_port,
      user = self._db_user,
      passwd = self._db_pass,
      db = self._db_db
      )
    self._connected = True

  def is_connected(self):
    return self._connected

  def _set_parameter(self, option, opt, value, parser):
    if opt == '--db-host':
      self._db_host = value
    elif opt == '--db-port':
      self._db_port = value
    elif opt == '--db-user':
      self._db_user = value
    elif opt == '--db-pass':
      self._db_pass = value
    elif opt == '--db-name':
      self._db_db = value

  def add_command_line_options(self, optparser):
    optparser.add_option('--db-host', metavar='HOST',
      default=self._db_host,
      help='MySQL host address, default %default',
      type='string', nargs=1, dest='db-host',
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-port', metavar='PORT',
      default=self._db_port,
      help='MySQL host port, default %default',
      type='string', nargs=1, dest='db-port',
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-user', metavar='USER',
      default=self._db_user,
      help='MySQL user, default %default',
      type='string', nargs=1, dest='db-user',
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-pass', metavar='PASS',
      default=self._db_pass,
      help='MySQL password, default %default',
      type='string', nargs=1, dest='db-pass',
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-name', metavar='DB',
      default=self._db_db,
      help='MySQL database name, default %default',
      type='string', nargs=1, dest='db-db',
      action='callback', callback=self._set_parameter)
