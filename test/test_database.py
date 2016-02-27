from quotapolicyd.database import connection as sql

def test_db():
  sql.connect()
