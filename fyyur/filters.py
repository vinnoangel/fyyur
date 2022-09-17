# Imports
#----------------------------------------------------------------------------#
import dateutil.parser
import babel
import collections

collections.Callable= collections.abc.Callable

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')


def convertToList(string):
    return string.split(',')


def convertToString(list):
    return ','.join(list)


def convertToBool(value):
    return True if value else False 