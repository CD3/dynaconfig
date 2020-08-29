
import sys, os

import pytest
from utils import *


from renderconftree.render import *
from renderconftree.exceptions import *

def test_simple():
  logging.info("exceptions")
  with pytest.raises(UnparsedExpressions) as e:
    rendered_data = render_tree( {'one':1, 'two':"$(one)"}, strict=True )

