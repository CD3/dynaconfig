import sys, os, timeit

import pytest

from renderconftree.read import *
from renderconftree.render import *

import utils

# import pudb; pu.db

def test_chained_references_performance():

  data = dict()

  data["v0"] = 10
  for i in range(1,40):
    data["v%s"%str(i)] = "$(${v%s} + 1)"%(i-1)

  print()

  timer = timeit.Timer( lambda: render_tree(data) )
  print(timer.timeit(1),'s')

  data = render_tree(data)
  for i in range(0,40):
    assert data["v%s"%str(i)] == 10+i


def test_reversed_chained_references_performance():

  data = dict()

  data["v40"] = 10
  for i in range(0,40):
    data["v%s"%str(i)] = "$(${v%s} + 1)"%(i+1)

  print()

  timer = timeit.Timer( lambda: render_tree(data) )
  print(timer.timeit(1),'s')

  data = render_tree(data)
  for i in range(0,41):
    # v40 == 10
    # v39 == 11
    # ...
    assert data["v%s"%str(i)] == 10+(40-i)

