import MySQLdb
import mock
import optparse
from quotapolicyd.database import DBLink

@mock.patch('quotapolicyd.database.MySQLdb')
def test_instantiate_link_and_connect_to_database(mocksql):
  '''Test the SQL connection routine.'''
  mocksql.connect.return_value = mock.sentinel.dblink
  sql = DBLink()
  assert not sql.is_connected()

  sql.connect()

  assert mocksql.connect.call_count == 1
  assert sql.is_connected()

  sql.connect()

  assert mocksql.connect.call_count == 1
  assert sql.is_connected()

@mock.patch('quotapolicyd.database.MySQLdb')
def test_parse_command_line_options(mocksql):
  '''Check that command line parameters are passed on appropriately.'''
  parser = optparse.OptionParser()

  sql = DBLink()
  sql.add_command_line_options(parser)
  parser.parse_args([
    '--db-host', mock.sentinel.host,
    '--db-port', '1234',
    '--db-user', mock.sentinel.user,
    '--db-pass', mock.sentinel.password,
    '--db-name', mock.sentinel.database])

  sql.connect()

  assert mocksql.connect.call_count == 1
  args, kwargs = mocksql.connect.call_args
  assert kwargs['host'] == mock.sentinel.host
  assert kwargs['port'] == 1234
  assert kwargs['user'] == mock.sentinel.user
  assert kwargs['passwd'] == mock.sentinel.password
  assert kwargs['db'] == mock.sentinel.database

def test_add_command_line_help():
  '''Check that command line parameters are registered in the parser.'''
  parser = mock.MagicMock()

  DBLink().add_command_line_options(parser)

  assert parser.add_option.called
  assert parser.add_option.call_count > 4
  for call in parser.add_option.call_args_list:
    assert call[1]['action'] == 'callback'

@mock.patch('quotapolicyd.database.MySQLdb')
def test_check_config_file_behaviour(mocksql):
  '''Check that default parameters are not active when configuration file is used.'''
  parser = optparse.OptionParser()

  sql = DBLink()
  sql.add_command_line_options(parser)
  parser.parse_args([
    '--db-conf', mock.sentinel.config,
    '--db-user', mock.sentinel.user])

  sql.connect()

  assert mocksql.connect.call_count == 1
  args, kwargs = mocksql.connect.call_args
  assert kwargs['read_default_file'] == mock.sentinel.config
  assert kwargs['user'] == mock.sentinel.user
  for undefined in ['host', 'port', 'passwd', 'db']:
    assert undefined not in kwargs

@mock.patch('quotapolicyd.database.MySQLdb')
def test_retrieve_user_information(mocksql):
  '''Test the function to retrieve information from the database.'''
  mocksql.connect.return_value. \
    cursor.return_value. \
    fetchone.return_value = mock.sentinel.dbresults

  sql = DBLink()
  user_info = sql.get_user_info(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  args, kwargs = mocksql.connect().cursor().execute.call_args
  assert args[1] == (mock.sentinel.user,)
  assert args[0].startswith("SELECT")
  assert ';' not in args[0]
  assert mocksql.connect().cursor().close.call_count == 1
  assert user_info == mock.sentinel.dbresults

@mock.patch('quotapolicyd.database.MySQLdb')
def test_retrieve_user_information_error_handling(mocksql):
  '''Test error handling in the function to retrieve information from the database.'''
  mocksql.connect.return_value.cursor.return_value. \
    execute.side_effect = MySQLdb.Error()
  mocksql.MySQLError = MySQLdb.MySQLError

  sql = DBLink()
  user_info = sql.get_user_info(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert user_info is None

@mock.patch('quotapolicyd.database.MySQLdb')
def test_create_user(mocksql):
  '''Test creating a user in the database.'''
  sql = DBLink()
  retval = sql.create_user(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  args, kwargs = mocksql.connect().cursor().execute.call_args
  assert args[1] == (mock.sentinel.user,)
  assert args[0].startswith("INSERT INTO")
  assert ';' not in args[0]
  assert mocksql.connect().commit.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_create_user_error_handling(mocksql):
  '''Test error handling on creating a user in the database.'''
  mocksql.connect.return_value.cursor.return_value. \
    execute.side_effect = MySQLdb.Error()
  mocksql.MySQLError = MySQLdb.MySQLError

  sql = DBLink()
  retval = sql.create_user(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert not retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_increment_user_counter(mocksql):
  '''Test incrementing the counter of a user.'''
  sql = DBLink()
  retval = sql.increment_user(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  args, kwargs = mocksql.connect().cursor().execute.call_args
  assert args[1] == (mock.sentinel.user,)
  assert args[0].startswith("UPDATE")
  assert ';' not in args[0]
  assert mocksql.connect().commit.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_increment_user_counter_error_handling(mocksql):
  '''Test error handling on incrementing the counter of a user.'''
  mocksql.connect.return_value.cursor.return_value. \
    execute.side_effect = MySQLdb.Error()
  mocksql.MySQLError = MySQLdb.MySQLError

  sql = DBLink()
  retval = sql.increment_user(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert not retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_increment_user_counter_and_lock(mocksql):
  '''Test incrementing the counter of a user and locking the account.'''
  sql = DBLink()
  retval = sql.increment_lock_user(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  args, kwargs = mocksql.connect().cursor().execute.call_args
  assert args[1] == (mock.sentinel.user,)
  assert args[0].startswith("UPDATE")
  assert ';' not in args[0]
  assert mocksql.connect().commit.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_increment_user_counter_and_lock_error_handling(mocksql):
  '''Test error handling on incrementing the counter of a user and locking the account.'''
  mocksql.connect.return_value.cursor.return_value. \
    execute.side_effect = MySQLdb.Error()
  mocksql.MySQLError = MySQLdb.MySQLError

  sql = DBLink()
  retval = sql.increment_lock_user(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert not retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_unlock_user(mocksql):
  '''Test unlocking a user.'''
  sql = DBLink()
  retval = sql.unlock_user_increase_limit(mock.sentinel.user, mock.sentinel.limit)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  args, kwargs = mocksql.connect().cursor().execute.call_args
  assert args[1] == (mock.sentinel.limit, mock.sentinel.user, mock.sentinel.user)
  assert args[0].startswith("UPDATE")
  assert ';' not in args[0]
  assert mocksql.connect().commit.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_unlock_user_error_handling(mocksql):
  '''Test error handling on unlocking a user.'''
  mocksql.connect.return_value.cursor.return_value. \
    execute.side_effect = MySQLdb.Error()
  mocksql.MySQLError = MySQLdb.MySQLError

  sql = DBLink()
  retval = sql.unlock_user_increase_limit(mock.sentinel.user, mock.sentinel.limit)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert not retval

#
# To run the test below you need to pass a MySQL configuration file to py.test
# with the  --live-database-config=...  command line parameter. Note that this
# will modify an existing database, so do not use on production systems!
#

def test_using_live_database_connect(dbconfig):
  '''Run tests on a live database.'''
  import datetime
  parser = optparse.OptionParser()

  sql = DBLink()
  sql.add_command_line_options(parser)
  parser.parse_args(['--db-conf', dbconfig])

  sql.connect()

  non_existent_user = sql.get_user_info('pytest_dummy_user_nonext')
  assert non_existent_user is None

  user1_name = 'pytest_dummy_user_1'
  user1 = sql.get_user_info(user1_name)
  assert user1 == {'authcount': 0L, 'dynlimit': 3L, 'lastseen': datetime.datetime(2016, 3, 2, 21, 34, 8), 'limit': 3L, 'username': user1_name, 'reset': 1L, 'unseen': 0L, 'locked': 'N'}
  user1_lastseen = user1['lastseen']

  user2_name = 'pytest_dummy_user_2'
  user2 = sql.get_user_info(user2_name)
  assert user2 == {'authcount': None, 'dynlimit': None, 'lastseen': None, 'limit': None, 'username': user2_name, 'reset': None, 'unseen': 1L, 'locked': None}

  sql.create_user(user2_name)
  user2 = sql.get_user_info(user2_name)
  assert user2['lastseen'] is not None
  del user2['lastseen']
  assert user2 == {'authcount': 1L, 'dynlimit': 100L, 'limit': 100L, 'username': user2_name, 'reset': 0L, 'unseen': 0L, 'locked': 'N'}

  for inc in [1L, 2L, 3L]:
    sql.increment_user(user1_name)
    user1 = sql.get_user_info(user1_name)
    assert user1['lastseen'] is not None
    assert user1['lastseen'] != user1_lastseen
    del user1['lastseen']
    assert user1 == {'authcount': inc, 'dynlimit': 3L, 'limit': 3L, 'username': user1_name, 'reset': 1L, 'unseen': 0L, 'locked': 'N'}

  sql.increment_lock_user(user1_name)
  user1 = sql.get_user_info(user1_name)
  del user1['lastseen']
  assert user1 == {'authcount': 4L, 'dynlimit': 3L, 'limit': 3L, 'username': user1_name, 'reset': 1L, 'unseen': 0L, 'locked': 'Y'}

  sql.unlock_user_increase_limit(user1_name, 20)
  user1 = sql.get_user_info(user1_name)
  del user1['lastseen']
  assert user1 == {'authcount': 4L, 'dynlimit': 20L, 'limit': 3L, 'username': user1_name, 'reset': 0L, 'unseen': 0L, 'locked': 'N'}
