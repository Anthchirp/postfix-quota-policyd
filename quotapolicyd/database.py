import MySQLdb
import MySQLdb.cursors
import threading

class db_link():
  def __init__(self):
    # Set some sensible defaults
    self.defaults = {
      '--db-host': '127.0.0.1',
      '--db-port': 3306,
      '--db-user': 'quotapolicyd',
      '--db-pass': 'quotapolicyd',
      '--db-name': 'quotapolicyd'
    }
    # Effective configuration
    self.config = {}

    self._connected = False
    self._db = None

  def connect(self):
    if self._connected: return
    self._db = MySQLdb.connect(
      host = self.config.get('--db-host', self.defaults.get('--db-host', None)),
      port = self.config.get('--db-port', self.defaults.get('--db-port', None)),
      user = self.config.get('--db-user', self.defaults.get('--db-user', None)),
      passwd = self.config.get('--db-pass', self.defaults.get('--db-pass', None)),
      db = self.config.get('--db-name', self.defaults.get('--db-name', None)),
      read_default_file = self.config.get('--db-conf', self.defaults.get('--db-conf', None))
    )
    self._connected = True

  def is_connected(self):
    return self._connected


  def get_user_info(self, username):
    '''SELECT username,
       smtplogin.username IS NULL AS unseen,
       smtplogin.locked,
       smtplogin.password != auth.password AS reset,
       smtplogin.authcount,
       smtplogin.limit,
       smtplogin.dynlimit,
       smtplogin.lastseen
  FROM auth LEFT OUTER JOIN smtplogin USING (username, source) WHERE username='$username'");'''
    return { 'username': username }

  def create_user(self, username):
    '''INSERT INTO smtplogin (username, source, password, authcount, lastseen) SELECT username, source, password, 1, NOW() FROM auth WHERE username = '$username' '''
    return True

  def increment_user(self, username):
    '''UPDATE smtplogin SET authcount = authcount + 1, lastseen = NOW() WHERE username='$username' '''
    return True

  def increment_lock_user(self, username):
    '''UPDATE smtplogin SET authcount = authcount + 1, lastseen = NOW(), locked = 'Y' WHERE username='$username' '''
    return True

  def unlock_user(self, username):
    '''UPDATE smtplogin SET locked = 'N', dynlimit = $newlimit, password = (SELECT password FROM auth WHERE username='$username') WHERE username='$username' '''
    return True


  def _set_parameter(self, option, opt, value, parser):
    '''callback function for optionparser'''
    self.config[opt] = value
    if opt == '--db-conf':
      self.defaults = {}

  def add_command_line_options(self, optparser):
    '''function to inject command line parameters'''
    optparser.add_option('--db-host', metavar='HOST',
      default=self.defaults.get('--db-host', None),
      help='MySQL host address, default %default',
      type='string', nargs=1,
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-port', metavar='PORT',
      default=self.defaults.get('--db-port', None),
      help='MySQL host port, default %default',
      type='int', nargs=1,
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-user', metavar='USER',
      default=self.defaults.get('--db-user', None),
      help='MySQL user, default %default',
      type='string', nargs=1,
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-pass', metavar='PASS',
      default=self.defaults.get('--db-pass', None),
      help='MySQL password, default %default',
      type='string', nargs=1,
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-name', metavar='DB',
      default=self.defaults.get('--db-name', None),
      help='MySQL database name, default %default',
      type='string', nargs=1,
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-conf', metavar='CNF',
      default=self.defaults.get('--db-conf', None),
      help='MySQL configuration file containing connection information, disables MySQL default values',
      type='string', nargs=1,
      action='callback', callback=self._set_parameter)
