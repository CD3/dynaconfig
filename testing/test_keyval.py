import sys, os, timeit

import pytest
from utils import Approx

from dynaconfig.read import *
from dynaconfig.file_parsers import *

import logging
logger = logging.getLogger('dynaconfig')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)


def test_simple():

  data = '''
  var1 = $(1)
  var2 = some string
  var3 = $(3)
  var4 = $(${var3} + pi + 2)
  var5 = $(${var4} + 2.0)
  nest1/var1 = $(11)
  nest1/var2 = $(${var3} + 12)
  nest1/var3 = $(${var1} + 12)
  nest1/var4 = $(${var3} + 12)
  nest1/var5 = $(${../nest1/var3} + 12)
  nest1/list1/0 = $(1)
  nest1/list1/1 = $(${0})
  nest1/list1/2 = $(3)
  nest1/nest2/var1 = $(111)
  nest1/nest2/var2 = $(112)
  nest1/nest2/var3 = $(${var1})
  nest1/nest2/var4 = $(${/var1})
  nest1/nest2/var5 = $(${/nest1/var1})
  '''

  data = readConfig( data , parser=lambda x : keyval.load(x) )


  assert data['var1'] == 1
  assert data['var2'] == 'some string'
  assert data['var3'] == 3
  assert data['var4'] ==  Approx(3 + 3.14159 + 2 )
  assert data['var5'] ==  Approx(3 + 3.14159 + 2 + 2.0 )
  assert data['nest1']['var1'] == 11
  assert data['nest1']['var2'] == 11 + 12 + 12
  assert data['nest1']['var3'] == 11 + 12
  assert data['nest1']['var4'] == 11 + 12 + 12
  assert data['nest1']['var5'] == 11 + 12 + 12
  assert data['nest1']['list1']['0'] == 1
  assert data['nest1']['list1']['1'] == 1
  assert data['nest1']['list1']['2'] == 3
  assert data['nest1']['nest2']['var1'] == 111
  assert data['nest1']['nest2']['var2'] == 112
  assert data['nest1']['nest2']['var3'] == 111
  assert data['nest1']['nest2']['var4'] == 1
  assert data['nest1']['nest2']['var5'] == 11


# import pudb; pu.db

def test_property_tree_style_keys():
  text = '''
emitters.0.irradiance=$("2 W/cm/cm" |> quant)
emitters.0.beam.profile.diameter=$("5 mm" |> quant)
emitters.0.power=$( context['emitters.0.irradiance']*(m.pi/4)*context['emitters.0.beam.profile.diameter']**2 |> to W |> mag)
  '''

  data = readConfig( text, parser=lambda x : keyval.load(x) )

  assert data['emitters.0.irradiance'].magnitude == 2
  assert data['emitters.0.beam.profile.diameter'].magnitude == 5
  assert data['emitters.0.power'] == Approx(2*3.14159*0.5*0.5/4)




