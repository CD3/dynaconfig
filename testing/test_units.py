import sys, os
import pytest

from renderconftree.render import *
from renderconftree.read import *
from utils import *

import logging
# logger = logging.getLogger('renderconftree')
# logger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# logger.addHandler(ch)

# import pudb; pu.db


def test_expression_substitution_with_quantity_filter():

  text = "$('10 cm' |> quant)"
  val = expression_substitution(text)
  val.magnitude == 10
  val.to("m").magnitude == Approx(0.1)
  

def test_adding_unit_support_example():
  data = '''
  # heat solver config file
  grid:
    x:
      min_q : -1 cm
      max_q : 5 mm
      min : $( '${min_q}' |> quant |> to m |> mag)
      max :  $( '${max_q}' |> quant |> to m |> mag)
      N   : 100
    y:
      min_q : 0 m
      max_q : 20 mm
      min : $( '${min_q}' |> quant |> to m |> mag)
      max : $( '${max_q}' |> quant |> to m |> mag)
      N   : 200
  time:
    start_q : 0 s
    stop_q : 10 s
    dt_q : 1 ms
    start : $( '${start_q}' |> quant |> to s |> mag)
    stop : $( '${stop_q}' |> quant |> to s |> mag)
    dt : $( '${dt_q}' |> quant |> to s |> mag)
  '''


  data = readConfig( data )

  assert data['grid']['x']['min'] == Approx(-0.01)
  assert data['grid']['x']['max'] == Approx(0.005)
  assert data['grid']['y']['min']+1 == Approx(1)
  assert data['grid']['y']['max'] == Approx(0.020)
  assert data['time']['start']+1 == Approx(1)
  assert data['time']['stop'] == Approx(10)
  assert data['time']['dt'] == Approx(0.001)



