import MySQLdb
import mock
import optparse
from quotapolicyd.database import DBLink

@mock.patch('quotapolicyd.database.MySQLdb')
def test_instantiate_link_and_connect_to_database(mocksql):
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
  parser = mock.MagicMock()

  DBLink().add_command_line_options(parser)

  assert parser.add_option.called
  assert parser.add_option.call_count > 4
  for call in parser.add_option.call_args_list:
    assert call[1]['action'] == 'callback'

@mock.patch('quotapolicyd.database.MySQLdb')
def test_check_config_file_behaviour(mocksql):
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
  sql = DBLink()
  retval = sql.create_user(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  args, kwargs = mocksql.connect().cursor().execute.call_args
  assert args[1] == (mock.sentinel.user,)
  assert args[0].startswith("INSERT INTO")
  assert ';' not in args[0]
  assert mocksql.connect().cursor().commit.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_create_user_error_handling(mocksql):
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
  sql = DBLink()
  retval = sql.increment_user(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  args, kwargs = mocksql.connect().cursor().execute.call_args
  assert args[1] == (mock.sentinel.user,)
  assert args[0].startswith("UPDATE")
  assert ';' not in args[0]
  assert mocksql.connect().cursor().commit.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_increment_user_counter_error_handling(mocksql):
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
  sql = DBLink()
  retval = sql.increment_lock_user(mock.sentinel.user)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  args, kwargs = mocksql.connect().cursor().execute.call_args
  assert args[1] == (mock.sentinel.user,)
  assert args[0].startswith("UPDATE")
  assert ';' not in args[0]
  assert mocksql.connect().cursor().commit.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_increment_user_counter_and_lock_error_handling(mocksql):
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
  sql = DBLink()
  retval = sql.unlock_user_increase_limit(mock.sentinel.user, mock.sentinel.limit)

  assert sql.is_connected()
  assert mocksql.connect.call_count == 1
  assert mocksql.connect().cursor().execute.call_count == 1
  args, kwargs = mocksql.connect().cursor().execute.call_args
  assert args[1] == (mock.sentinel.limit, mock.sentinel.user, mock.sentinel.user)
  assert args[0].startswith("UPDATE")
  assert ';' not in args[0]
  assert mocksql.connect().cursor().commit.call_count == 1
  assert mocksql.connect().cursor().close.call_count == 1
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_unlock_user_error_handling(mocksql):
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

def test_using_live_database_do_stuff(dbconfig):
  print "TEST:", dbconfig

