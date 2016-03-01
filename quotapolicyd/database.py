import MySQLdb
import MySQLdb.cursors
import threading

class DBLink():
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

    # single-threaded database access
    self._lock = threading.Lock()

  def connect(self):
    with self._lock:
      if self._connected: return
      kwargs = { 'cursorclass': MySQLdb.cursors.DictCursor }
      for kw, val in [('host', '--db-host'),
                      ('port', '--db-port'),
                      ('user', '--db-user'),
                      ('passwd', '--db-pass'),
                      ('db', '--db-name'),
                      ('read_default_file', '--db-conf')]:
        set_value = self.config.get(val, self.defaults.get(val))
        if set_value is not None:
          kwargs[kw] = set_value
      self._db = MySQLdb.connect(**kwargs)
      self._db.raise_on_warnings = True
      self._connected = True

  def is_connected(self):
    return self._connected


  def get_user_info(self, username):
    self.connect()
    with self._lock:
      try:
        c=self._db.cursor()
        c.execute("""SELECT username,
          smtplogin.username IS NULL AS unseen,
          smtplogin.locked,
          smtplogin.password != auth.password AS reset,
          smtplogin.authcount,
          smtplogin.limit,
          smtplogin.dynlimit,
          smtplogin.lastseen
          FROM auth
          LEFT OUTER JOIN smtplogin USING (username, source)
          WHERE username=%s""", (username,))
        result = c.fetchone()
        return result
      except MySQLdb.MySQLError, e:
        # TODO: errors should be handled properly at some point
        print e
        return None
      finally:
        c.close()

  def create_user(self, username):
    self.connect()
    with self._lock:
      try:
        c=self._db.cursor()
        c.execute("""INSERT INTO smtplogin
          (username, source, password, authcount, lastseen)
          SELECT username, source, password, 1, NOW()
            FROM auth
            WHERE username=%s""", (username,))
        c.commit()
        return True
      except MySQLdb.MySQLError, e:
        # TODO: errors should be handled properly at some point
        print e
        return False
      finally:
        c.close()

  def increment_user(self, username):
    self.connect()
    with self._lock:
      try:
        c=self._db.cursor()
        c.execute("""UPDATE smtplogin
           SET authcount = authcount + 1, lastseen = NOW()
           WHERE username=%s""", (username,))
        c.commit()
        return True
      except MySQLdb.MySQLError, e:
        # TODO: errors should be handled properly at some point
        print e
        return False
      finally:
        c.close()

  def increment_lock_user(self, username):
    self.connect()
    with self._lock:
      try:
        c=self._db.cursor()
        c.execute("""UPDATE smtplogin
           SET authcount = authcount + 1, lastseen = NOW(), locked = 'Y'
           WHERE username=%s""", (username,))
        c.commit()
        return True
      except MySQLdb.MySQLError, e:
        # TODO: errors should be handled properly at some point
        print e
        return False
      finally:
        c.close()

  def unlock_user_increase_limit(self, username, newlimit):
    self.connect()
    with self._lock:
      try:
        c=self._db.cursor()
        c.execute("""UPDATE smtplogin
           SET locked = 'N', dynlimit = %s, password = (
             SELECT password
             FROM auth
             WHERE username = %s
           )
           WHERE username=%s""", (newlimit, username, username))
        c.commit()
        return True
      except MySQLdb.MySQLError, e:
        # TODO: errors should be handled properly at some point
        print e
        return False
      finally:
        c.close()

  def _set_parameter(self, option, opt, value, parser):
    '''callback function for optionparser'''
    del option, parser # unused
    self.config[opt] = value
    if opt == '--db-conf':
      self.defaults = {}

  def add_command_line_options(self, optparser):
    '''function to inject command line parameters'''
    optparser.add_option('--db-host', metavar='HOST',
      default=self.defaults.get('--db-host'),
      help='MySQL host address, default %default',
      type='string', nargs=1,
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-port', metavar='PORT',
      default=self.defaults.get('--db-port'),
      help='MySQL host port, default %default',
      type='int', nargs=1,
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-user', metavar='USER',
      default=self.defaults.get('--db-user'),
      help='MySQL user, default %default',
      type='string', nargs=1,
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-pass', metavar='PASS',
      default=self.defaults.get('--db-pass'),
      help='MySQL password, default %default',
      type='string', nargs=1,
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-name', metavar='DB',
      default=self.defaults.get('--db-name'),
      help='MySQL database name, default %default',
      type='string', nargs=1,
      action='callback', callback=self._set_parameter)
    optparser.add_option('--db-conf', metavar='CNF',
      default=self.defaults.get('--db-conf'),
      help='MySQL configuration file containing connection information, disables MySQL default values',
      type='string', nargs=1,
      action='callback', callback=self._set_parameter)
