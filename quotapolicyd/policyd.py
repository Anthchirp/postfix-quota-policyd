import database
from optparse import OptionParser, SUPPRESS_HELP
import log
import sys

class Policyd():
  def __init__(self):
    self.sql = database.DBLink()
    self.log = log.Logger()

  def run(self):
    parser = OptionParser()
    #parser.add_option("-v", action="store_true", dest="verbose",
    #                  help="be moderately verbose")
    parser.add_option("-?", help=SUPPRESS_HELP, action="help")

    self.sql.add_command_line_options(parser)
    opts, args = parser.parse_args()

if __name__ == "__main__":
  Policyd().run()
