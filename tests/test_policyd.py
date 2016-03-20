import mock
import quotapolicyd.policyd

@mock.patch('quotapolicyd.policyd.OptionParser')
@mock.patch('quotapolicyd.policyd.database')
@mock.patch('quotapolicyd.policyd.log')
def test_aggregate_command_line_help(log, database, optparse):
  '''Check that modules (database/log) add command line parameters.'''
  optparse().parse_args.return_value = ([], [])

  quotapolicyd.policyd.Policyd().run()

  database.DBLink().add_command_line_options.assert_called_once_with(optparse())
  log.Logger().add_command_line_options.assert_called_once_with(optparse())
  assert optparse().add_option.called # command line help flag
