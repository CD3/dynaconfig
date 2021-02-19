import sys, os
import pytest

from dynaconfig.render import *
import yaml

from utils import *

import pprint
#logging.basicConfig( level=logging.DEBUG )

def test_basic_rendering():
  text = '''
  global:
    size :
      x : 101
      y : 201
  simulations:
    - name : "${Nx} x ${Ny} grid for ${Nt} time-steps"
      Nt : 20
      Nx : "10"
      Ny : "20"
      Nt : 20
    - name : "${Nx} x ${Ny} grid for ${Nt} time-steps"
      xmin : 0
      xmax : 1
      Nx : ${/global/size/x}
      dx : $( ( ${xmax}-${xmin} ) / ( ${Nx} - 1 ) )
      ymin : -1
      ymax : 1
      Ny : ${/global/size/y}
      dy : $( (${ymax}-${ymin}) / ( ${/global/size/y} - 1 ) )

  '''

  tree = fspathtree(yaml.safe_load( text ))

  assert tree['/global/size/x'] == 101
  assert tree['/global/size/y'] == 201
  assert tree['/simulations/0/name'] == "${Nx} x ${Ny} grid for ${Nt} time-steps"
  assert tree['/simulations/0/Nt'] == 20
  assert tree['/simulations/0/Nx'] == '10'
  assert tree['/simulations/0/Ny'] == '20'



  tree = render_tree(tree)

  assert tree['/global/size/x'] == 101
  assert tree['/global/size/y'] == 201
  assert tree['/simulations/0/name'] == "10 x 20 grid for 20 time-steps"
  assert tree['/simulations/0/Nt'] == 20
  assert tree['/simulations/0/Nx'] == '10'
  assert tree['/simulations/0/Ny'] == '20'

  assert tree['/simulations/1/Nx'] == 101
  assert tree['/simulations/1/Ny'] == 201
  assert tree['/simulations/1/xmin'] == 0
  assert tree['/simulations/1/xmax'] == 1
  assert tree['/simulations/1/dx'] == Approx(0.01)
  assert tree['/simulations/1/dy'] == Approx(0.01)


def test_property_tree_style_keys():
  d = { 'l11.l12.var1' : 1,
      'l11.l12.var2' : 2,
      'l11.l12.var3' : '${l11.l12.var2}',
      'l11.l12.var4' : '$( ${l11.l12.var2}*2)'}

  t = render_tree(d)

  assert t['l11.l12.var1'] == 1
  assert t['l11.l12.var2'] == 2
  assert t['l11.l12.var3'] == 2
  assert t['l11.l12.var4'] == 4

