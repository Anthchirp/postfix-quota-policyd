import mock
import optparse

from quotapolicyd.database import db_link

@mock.patch('quotapolicyd.database.MySQLdb')
def test_instantiate_link_and_connect_to_database(mocksql):
  mocksql.connect.return_value = mock.sentinel.dblink
  sql = db_link()
  assert not sql.is_connected()

  sql.connect()

  assert mocksql.connect.called == 1
  assert sql._db == mock.sentinel.dblink
  assert sql.is_connected()

@mock.patch('quotapolicyd.database.MySQLdb')
def test_parse_command_line_options(mocksql):
  parser = optparse.OptionParser()

  sql = db_link()
  sql.add_command_line_options(parser)
  parser.parse_args([
    '--db-host', mock.sentinel.host,
    '--db-port', '1234',
    '--db-user', mock.sentinel.user,
    '--db-pass', mock.sentinel.password,
    '--db-name', mock.sentinel.database])

  sql.connect()

  assert mocksql.connect.called == 1
  args, kwargs = mocksql.connect.call_args
  assert kwargs['host'] == mock.sentinel.host
  assert kwargs['port'] == 1234
  assert kwargs['user'] == mock.sentinel.user
  assert kwargs['passwd'] == mock.sentinel.password
  assert kwargs['db'] == mock.sentinel.database

@mock.patch('quotapolicyd.database.MySQLdb')
def test_check_config_file_behaviour(mocksql):
  parser = optparse.OptionParser()

  sql = db_link()
  sql.add_command_line_options(parser)
  parser.parse_args([
    '--db-conf', mock.sentinel.config,
    '--db-user', mock.sentinel.user])

  sql.connect()

  assert mocksql.connect.called == 1
  args, kwargs = mocksql.connect.call_args
  assert kwargs['read_default_file'] == mock.sentinel.config
  assert kwargs['user'] == mock.sentinel.user
  for undefined in ['host', 'port', 'passwd', 'db']:
    assert undefined not in kwargs

@mock.patch('quotapolicyd.database.MySQLdb')
def test_retrieve_user_information(mocksql):
  mocksql.connect().cursor().fetchone.return_value = mock.sentinel.dbresults

  sql = db_link()
  user_info = sql.get_user_info(mock.sentinel.user)

  assert mocksql.connect.called == 1
  assert sql.is_connected()

  assert mocksql.connect().cursor().execute.called == 1
  args, kwargs = mocksql.connect().cursor().execute.call_args
  assert args[1] == (mock.sentinel.user,)
  assert args[0].startswith("SELECT")
  assert mocksql.connect().cursor().close.called == 1
  assert user_info == mock.sentinel.dbresults 

@mock.patch('quotapolicyd.database.MySQLdb')
def test_create_user(mocksql):
  sql = db_link()
  sql.connect()

  retval = sql.create_user(mock.sentinel.user)
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_increment_user_counter(mocksql):
  sql = db_link()
  sql.connect()

  retval = sql.increment_user(mock.sentinel.user)
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_increment_user_counter_and_lock(mocksql):
  sql = db_link()
  sql.connect()

  retval = sql.increment_lock_user(mock.sentinel.user)
  assert retval

@mock.patch('quotapolicyd.database.MySQLdb')
def test_unlock_user(mocksql):
  sql = db_link()
  sql.connect()

  retval = sql.unlock_user(mock.sentinel.user)
  assert retval
