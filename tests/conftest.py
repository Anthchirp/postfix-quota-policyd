def pytest_addoption(parser):
  parser.addoption('--live-database-config', metavar='CNF', type="string", nargs=1,
    help='run live database tests. CNF points to a MySQL configuration file containing connection information')

def pytest_generate_tests(metafunc):
  if 'dbconfig' in metafunc.fixturenames:
    if metafunc.config.option.live_database_config:
      metafunc.parametrize('dbconfig', [metafunc.config.option.live_database_config])
    else:
      metafunc.parametrize('dbconfig', [])
