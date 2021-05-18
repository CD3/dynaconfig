import sys, os
import pytest

from dynaconfig.validation.models import *

def test_xygrid_validation():

  config = {
      "grid" : { "x" : { "min" : 0, "max" : 1, "N" : 10 },
                 "y" : { "min" : 1, "max" : 2, "N" : 2 }
      }
      }

  grid = XYGrid( **config["grid"] )

  assert type(grid.x.max) == float
  assert grid.x.max == 1
  assert type(grid.y.max) == float
  assert grid.y.max == 2


  config = {
      "grid" : { "x" : { "min" : 0, "max" : 1, "N" : 10 }
      }
      }

  with pytest.raises(pydantic.ValidationError):
    grid = XYGrid( **config["grid"] )


