#! /usr/bin/python

import sys, os

from renderconftree.read import *
from renderconftree.exceptions import *
from argparse import ArgumentParser
import logging

def ft(fn):
  '''Return filetype from filename.'''
  if fn.endswith(".dync"):
    fn = fn[:-5]
  if fn.endswith(".t"):
    fn = fn[:-2]

  if fn.endswith("yaml") or fn.endswith("yml"):
    return "yaml"
  if fn.endswith("json"):
    return "json"
  if fn.endswith("ini"):
    return "ini"
  if fn.endswith("txt"):
    return "keyval"


def main():
  parser = ArgumentParser(description="Render a set of config files.")

  parser.add_argument("infile",
                      action="store",
                      help="Config file to process." )

  parser.add_argument("-f", "--from",
                      dest="_from",
                      action="store",
                      default=None,
                      help="Input file format." )

  parser.add_argument("-t", "--to",
                      dest="_to",
                      action="store",
                      default=None,
                      help="Output file format." )

  parser.add_argument("-o", "--output",
                      action="store",
                      default="-",
                      help="Output file",)

  parser.add_argument("-i", "--ignore-unparsed-expressions",
                      action="store_true",
                      help="Ignore errors related to unparsed expressions in the config file." )

  parser.add_argument("-d", "--debug",
                      action="store_true",
                      help="Enable debug output." )


  args = parser.parse_args()

  logger = logging.getLogger('renderconftree')
  if args.debug:
    logger.setLevel(logging.DEBUG)
  else:
    logger.setLevel(logging.INFO)

  ch = logging.StreamHandler()
  logger.addHandler(ch)

  outfile = args.output
  with open(args.infile, 'r') as f:
    text = f.read()

  ifmt = ft(args.infile)
  if args._from is not None:
    ifmt = args._from.lower()

  ofmt = ft(args.output)
  if args._to is not None:
    ofmt = args._to.lower()

  if ifmt is None:
    ifmt = "yaml"
  if ofmt is None:
    ofmt = "yaml"

  print(ifmt,'->',ofmt)

  if ifmt == "yaml":
    loader = yaml.safe_load
  elif ifmt == "json":
    loader = json.loads
  elif ifmt == "ini":
    loader = ini.load
  elif ifmt == "keyval":
    loader = keyval.load
  else:
    # default
    loader = yaml.safe_load

  if ofmt == "yaml":
    dumper = yaml.dump
  elif ofmt == "json":
    dumper = json.dumps
  elif ofmt == "ini":
    dumper = ini.dump
  elif ofmt == "keyval":
    dumper = keyval.dump
  else:
    # default
    dumper = yaml.dump


  try:
    config = readConfig( text, parser=loader, ignore_unparsed_expressions=args.ignore_unparsed_expressions )
  except UnparsedExpressions as e:
    print("Configuration file contained expressions that did not get expanded.")
    print(e)
    sys.exit(1)
  except Exception as e:
    print("There was an error rendeing the configuration file")
    print(e)
    sys.exit(2)


  text = dumper( config )

  if outfile == '-':
    print(text)
  else:
    with open(outfile, 'w') as f:
      f.write(text)

