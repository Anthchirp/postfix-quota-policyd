import mock
import optparse

from quotapolicyd.database import db_link

@mock.patch('quotapolicyd.database.MySQLdb')
def test_instantiate_link_and_connect_to_database(mocksql):
  sql = db_link()
  sql.connect()
  assert mocksql.connect.called == 1

@mock.patch('quotapolicyd.database.MySQLdb')
def test_parse_command_line_options(mocksql):
  mocksql.connect.return_value = mock.sentinel.dblink
  parser = optparse.OptionParser()

  sql = db_link()
  sql.add_command_line_options(parser)
  parser.parse_args([
    '--db-host', mock.sentinel.host,
    '--db-port', mock.sentinel.port,
    '--db-user', mock.sentinel.user,
    '--db-pass', mock.sentinel.password,
    '--db-name', mock.sentinel.database])

  assert not sql.is_connected()
  sql.connect()

  assert mocksql.connect.called == 1
  args, kwargs = mocksql.connect.call_args
  assert kwargs['host'] == mock.sentinel.host
  assert kwargs['port'] == mock.sentinel.port
  assert kwargs['user'] == mock.sentinel.user
  assert kwargs['passwd'] == mock.sentinel.password
  assert kwargs['db'] == mock.sentinel.database
  assert sql._db == mock.sentinel.dblink
  assert sql.is_connected()
