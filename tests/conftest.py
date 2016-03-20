def pytest_addoption(parser):
  '''Add command line option to add a configuration file to run the live database tests.'''
  parser.addoption('--live-database-config', metavar='CNF', type="string", nargs=1,
    help='run live database tests. CNF points to a MySQL configuration file containing connection information')

def pytest_generate_tests(metafunc):
  '''Run live database tests only when a configuration file is specified.'''
  if 'dbconfig' in metafunc.fixturenames:
    if metafunc.config.option.live_database_config:
      metafunc.parametrize('dbconfig', metafunc.config.option.live_database_config)
    else:
      metafunc.parametrize('dbconfig', [])
