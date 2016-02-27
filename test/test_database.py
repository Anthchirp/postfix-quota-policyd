import mock

@mock.patch('quotapolicyd.database.MySQLdb')
def test_db(sql_mock):
  from quotapolicyd.database import connection as sql
  sql.connect()
