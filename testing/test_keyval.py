import sys, os, timeit

import pytest
from utils import Approx

from renderconftree.read import *
from renderconftree.file_parsers import *

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


