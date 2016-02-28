import mock
import quotapolicyd.policyd

@mock.patch('quotapolicyd.policyd.OptionParser')
@mock.patch('quotapolicyd.policyd.database')
def test_aggregate_command_line_help(database, optparse):
  optparse().parse_args.return_value = ([], [])

  quotapolicyd.policyd.policyd().run()

  assert database.db_link().add_command_line_options.called_once_with(optparse())
  assert optparse().add_option.called > 0
