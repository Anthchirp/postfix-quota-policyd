from database import connection as sql
from optparse import OptionParser, SUPPRESS_HELP
import sys

parser = OptionParser()
#parser.add_option("-v", action="store_true", dest="verbose",
#                  help="be moderately verbose")
parser.add_option("-?", help=SUPPRESS_HELP, action="help")

sql.add_command_line_options(parser)

opts, args = parser.parse_args()

