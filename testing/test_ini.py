#! /usr/bin/python

import sys, os

import configparser, io
from dynaconfig.read import *

from utils import *

import pytest

# ini parser loads everything as a string...

#logging.basicConfig( level=logging.DEBUG )

def test_simple_ini():
  # the ini parser parses all values as strings.
  # so if we want values to be numbers, we have to put them into expressions.
  data = '''
[main]
var1 = $(1)
var2 = some string
var3 = $(3)
var4 = $(${var3} + math.pi + 2)
var5 = $(${var4} + 2.0)
[nest1]
var1 = $(11)
var2 = $(${var3} + 12)
var3 = $(${var1} + 12)
var4 = $(${var3} + 12)
var5 = $(${/nest1/var3} + 12)
'''

  data = readConfig( data, parser = ini.load, ignore_unparsed_expressions = True )

  assert data['main']['var1'] == 1
  assert data['main']['var2'] == 'some string'
  assert data['main']['var3'] == 3
  assert data['main']['var4'] == Approx(3 + 3.14159 + 2)
  assert data['main']['var5'] == Approx(3 + 3.14159 + 2 + 2.0)
  assert data['nest1']['var1'] == 11
  assert data['nest1']['var2'] == 11 + 12 + 12
  assert data['nest1']['var3'] == 11 + 12
  assert data['nest1']['var4'] == 11 + 12 + 12
  assert data['nest1']['var5'] == 11 + 12 + 12

@pytest.mark.skip(reason="need to figure out how to get ini to parse numbers as numbers.")
def test_configParser():
  '''A vanilla configparser example'''
  text= '''
[main]
var1 = 1
var2 = some string
var3 = 3
var4 = %(var3)s
var5 = %(var4)s
[nest1]
var1 = 11
var2 = %(var3)s
var3 = %(var1)s
var4 = %(var3)s
#var5 = %(main.var3)s # this will cause an interpolation error
'''

  parser = configparser.ConfigParser()
  f = io.StringIO(text)
  parser.readfp( f )
  f.close()

  data = dict()
  for sec in parser.sections():
    data[sec] = dict()
    for opt in parser.options(sec):
      data[sec][opt] = parser.get( sec, opt )

