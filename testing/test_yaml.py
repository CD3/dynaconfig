#! /usr/bin/python

import sys, os, timeit, pprint

import pytest

from renderconftree.read import *

from utils import *

# import pudb; pu.db

def test_simple_yaml():
  data = '''
  var1 : 1
  var2 : some string
  var3 : 3
  var4 : "$(${var3} + pi + 2)"
  var5 : "$(${var4} + 2.0)"
  nest1 : &nest
    var1 : 11
    var2 : "$(${var3} + 12)"
    var3 : "$(${var1} + 12)"
    var4 : "$(${var3} + 12)"
    var5 : "$(${../nest1/var3} + 12)"
    list1 :
      - 01
      - "$(${0})"
      - 03
    nest2 :
      var1 : 111
      var2 : 112
      var3 : "$(${var1})"
      var4 : "$(${/var1})"
      var5 : "${/nest1/var1}"
  '''

  data = readConfig( data )

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
  assert data['nest1']['list1'][0] == 1
  assert data['nest1']['list1'][1] == 1
  assert data['nest1']['list1'][2] == 3
  assert data['nest1']['nest2']['var1'] == 111
  assert data['nest1']['nest2']['var2'] == 112
  assert data['nest1']['nest2']['var3'] == 111
  assert data['nest1']['nest2']['var4'] == 1
  assert data['nest1']['nest2']['var5'] == 11

def test_large_yaml():
  data = '''
  var1 : 1
  var2 : some string
  var3 : 3
  var4 : '$(${var3} + pi + 2)'
  var5 : '$(${var4} + 2.0)'
  nest1 : &nest
    var1 : 11
    var2 : '$(${var3} + 12)'
    var3 : '$(${var1} + 12)'
    var4 : '$(${var3} + 12)'
    var5 : '$(${../nest1/var3} + 12)'
    nest2 :
      var1 : 111
      var2 : 112
      var3 : '$(${var1})'
      var4 : '$(${/var1})'
      var5 : '$(${/nest1/var1})'
  nest2 :
    << : *nest
  nest3 :
    << : *nest
  nest4 :
    << : *nest
  nest5 :
    << : *nest
  nest6 :
    << : *nest
  nest7 :
    << : *nest
  nest8 :
    << : *nest
  nest9 :
    << : *nest
  nest10 :
    << : *nest
  nest10 :
    << : *nest
  nest11 :
    << : *nest
  nest12 :
    << : *nest
  nest13 :
    << : *nest
  nest14 :
    << : *nest
  nest15 :
    << : *nest
  '''


  data = readConfig( data )

  assert data['var1'] == 1
  assert data['var2'] == 'some string'
  assert data['var3'] == 3
  assert data['var4'] == Approx( 3 + 3.14159 + 2 )
  assert data['var5'] == Approx( 3 + 3.14159 + 2 + 2.0 )
  assert data['nest10']['var1'] == 11
  assert data['nest10']['var2'] == 11 + 12 + 12
  assert data['nest10']['var3'] == 11 + 12
  assert data['nest10']['var4'] == 11 + 12 + 12
  assert data['nest10']['var5'] == 11 + 12 + 12
  assert data['nest10']['nest2']['var1'] == 111
  assert data['nest10']['nest2']['var2'] == 112
  assert data['nest10']['nest2']['var3'] == 111
  assert data['nest10']['nest2']['var4'] == 1
  assert data['nest10']['nest2']['var5'] == 11
  assert data['nest15']['nest2']['var5'] == 11

@pytest.mark.skip(reason="need to re-implement include function.")
def test_includes():
  nesteddata = { 'one' : 1, 'two' : 2 }

  data = r'''
  var1 : 1
  var2 : some string
  nest1 : include('example.yaml')
  nest2 : include('example.yaml')
  '''

  with open('example.yaml','w') as f:
    f.write(yaml.dump(nesteddata))

  data = readConfig( data )

  assert data['nest1']['one'] == 1
  assert data['nest1']['two'] == 2
  assert data['nest2']['one'] == 1
  assert data['nest2']['two'] == 2

@pytest.mark.skip(reason="need to re-implement datatable function.")
def test_datatable():
  with open('example-data.txt', 'w') as f:
    f.write('''
    # units: cm 1/cm
    1.0 4
    1.1 3
    1.2 2
    ''')

  data = r'''
  var1 : 1
  var2 : some string
  data : DataTable('example-data.txt')
  '''

  data = readConfig( data )

  assert data['data'](0,0) == 1.0
  assert data['data'](0,1) == 4
  assert data['data'](1,0) == 1.1
  assert data['data'](1,1) == 3
  assert data['data'](2,0) == 1.2
  assert data['data'](2,1) == 2

def test_passthrough():
  '''test that a config file containing no template expressions works'''

  data = '''
  # heat solver config file
  grid:
    x:
      min : 0
      max : 10
      N   : 100
    y:
      min : 0
      max : 20
      N   : 200
  time:
    start : 0
    stop : 10
    dt : 0.001
  '''


  data = readConfig( data )

  assert data['grid']['x']['min'] == 0
  assert data['grid']['x']['max'] == 10
  assert data['grid']['x']['N']   == 100
  assert data['grid']['y']['min'] == 0
  assert data['grid']['y']['max'] == 20
  assert data['grid']['y']['N']   == 200
  assert data['time']['start']    == 0
  assert data['time']['stop']     == 10
  assert data['time']['dt']       == 0.001

def test_physicsy():
  '''test a config typical of physics simulations'''
  data = '''
  # heat solver config file
  res: 0.001
  grid:
    x:
      min : 0
      max : 10
      N   : $( (${max} - ${min})/${/res} )
    y:
      min : 0
      max : $(2*${../x/max})
      N   : $( (${max} - ${min})/${/res} )
    z:
      min : 0
      max : $(2*${../y/max})
      N   : $( (${max} - ${min})/${/res} )
  time:
    start : 0
    stop : $(math.pow(10,2))
    dt : 0.001
  '''


  data = readConfig( data, return_fspathtree=True )
  

  assert data['/grid/x/min'] == 0
  assert data['/grid/x/max'] == 10
  assert data['/grid/x/N']   == 10000
  assert data['/grid/y/min'] == 0
  assert data['/grid/y/max'] == 20
  assert data['/grid/y/N']   == 20000
  assert data['/grid/z/min'] == 0
  assert data['/grid/z/max'] == 40
  assert data['/grid/z/N']   == 40000
  assert data['/time/start'] == 0
  assert data['/time/stop']  == 100
  assert data['/time/dt']    == 0.001

@pytest.mark.skip(reason="need to port to new render function.")
def test_datatable2():
  with open('abscoe-data.txt', 'w') as f:
    f.write('''
    # units: nm 1/cm
    400 100
    450 200
    500 300
    550 400
    600 500
    650 600
    700 700
    750 800
    ''')

  data = '''
  {{py:
import math
  }}
  res: 0.001
  wavelength : 500 nm
  grid:
    x:
      min : 0
      max : 10
      N   : '{{ (c["max",int] - c["min",int])/c["/res"] }}'
  time:
    start : 0
    stop : {{math.pow(10,2)}}
    dt : 0.001
  materials :
    - desc : 'absorbing material'
      abscoe_data : DataTable('abscoe-data.txt')
      abscoe :
        - "{{ c['../abscoe_data'].rowstr( c['/wavelength'], 1, '1/cm' ) }}"
  '''

  data = readConfig( data, return_DataTree=True )

  # pprint.pprint(data.data)


  assert data['/materials/0/abscoe/0'] == "500 300.0"
