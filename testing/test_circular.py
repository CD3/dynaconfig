#! /usr/bin/python

import sys, os, json
import pytest

from dynaconfig.read import *

import utils

#logging.basicConfig(level=logging.DEBUG)

def test_circular_deps():

    data = '''
    var1 : 1
    var2 : "${var3}"
    var3 : "${var2}"
    nest1 :
      var1 : 11
      var2 : 12
      nest2 :
        var1 : 111
        var2 : 112
    '''

    with pytest.raises(CircularDependency):
      data = readConfig( data )





