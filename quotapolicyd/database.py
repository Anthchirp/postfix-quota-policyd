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


  def read_user_information(self, username):
    '''SELECT username,
       smtplogin.username IS NULL AS unseen,
       smtplogin.locked,
       smtplogin.password != auth.password AS reset,
       smtplogin.authcount,
       smtplogin.limit,
       smtplogin.dynlimit,
       smtplogin.lastseen
  FROM auth LEFT OUTER JOIN smtplogin USING (username, source) WHERE username='$username'");'''
    pass

  def create_user(self, username):
    '''INSERT INTO smtplogin (username, source, password, authcount, lastseen) SELECT username, source, password, 1, NOW() FROM auth WHERE username = '$username' '''
    pass

  def unlock_user(self, username):
    '''UPDATE smtplogin SET locked = 'N', dynlimit = $newlimit, password = (SELECT password FROM auth WHERE username='$username') WHERE username='$username' '''
    pass

  def increment_user_counter(self, username):
    '''UPDATE smtplogin SET authcount = authcount + 1, lastseen = NOW() WHERE username='$username' '''
    pass

  def lock_user(self, username):
    '''UPDATE smtplogin SET authcount = authcount + 1, lastseen = NOW(), locked = 'Y' WHERE username='$username' '''
    pass


  def _set_parameter(self, option, opt, value, parser):
    '''callback function for optionparser'''
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
    '''function to inject command line parameters'''
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
