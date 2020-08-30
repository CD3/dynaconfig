import sys, os
import pytest

from renderconftree.render import *
from fspathtree import fspathtree
from utils import *

import logging
# logger = logging.getLogger('renderconftree')
# logger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# logger.addHandler(ch)

# import pudb; pu.db

def test_variable_parser():

  text = ">>${var1}||${var2<<${var3}"
  results = parsers.variables.parse_string(text)
  result = next(results)
  assert result[0] == "var1"
  assert result[1] == 2
  assert result[2] == 9
  result = next(results)
  assert result[0] == "var3"
  assert result[1] == 19
  assert result[2] == 26


  text = ">>${  ${var1} } }==${var2} <<"
  results = parsers.variables.parse_string(text)
  result = next(results)
  assert result[0] == "var1"
  assert result[1] == 6
  assert result[2] == 13

  result = next(results)
  assert result[0] == "var2"
  assert result[1] == 19
  assert result[2] == 26


def test_expression_parser():
  text = ">>$( 1 + ${var1} )<<$(exp() + 1)"
  results = parsers.expressions.parse_string(text)
  result = next(results)
  assert result[0] == "1 + ${var1}"
  assert result[1] == 2
  assert result[2] == 18

  result = next(results)
  assert result[0] == "exp() + 1"
  assert result[1] == 20
  assert result[2] == 32

  text = ">>$(1 + $( 2 + $( exp() + ${var1} ) ) )<<"
  results = parsers.expressions.parse_string(text)
  result = next(results)
  assert result[0] == "1 + $( 2 + $( exp() + ${var1} ) )"
  assert result[1] == 2
  assert result[2] == 39

  
  with pytest.raises(StopIteration):
    result = next(results)

  text = ">>$(1 + 1 |> str )<<"
  results = parsers.expressions.parse_string(text)
  result = next(results)
  assert result[0] == "1 + 1"
  assert result[1] == 2
  assert result[2] == 18
  assert "str" in result[3]

def test_variable_expansion():

  context = {'var1': "inserted", 'var3' : "==$(x/y)==", 'l2' : {'var1':1} }
  assert variable_expansion(">>${var2}<<",context) == ">>${var2}<<"
  assert variable_expansion(">>${var1}<<",context) == ">>inserted<<"
  assert variable_expansion(">>${var1 }<<",context) == ">>inserted<<"
  assert variable_expansion(">>{var1}<<",context) == ">>{var1}<<"
  assert variable_expansion(">>${var3}<<",context,do_not_expand_if_value_contains_expression=True) == ">>${var3}<<"
  assert variable_expansion(">>${var3}<<",context) == ">>==$(x/y)==<<"
  assert variable_expansion(">>${l1/var1}<<",context) == ">>${l1/var1}<<"
  assert "l2/var1" in fspathtree(context)
  assert variable_expansion(">>${l2/var1}<<",fspathtree(context)) == ">>1<<"
  assert variable_expansion(">>${l2/var1}<<",fspathtree(context)['l2']) == ">>${l2/var1}<<"
  assert variable_expansion(">>${/l2/var1}<<",fspathtree(context)['l2']) == ">>1<<"
  assert variable_expansion(">>${../var1}<<",fspathtree(context)['l2']) == ">>inserted<<"

  assert variable_expansion(">>${var1} and ${../var1}<<",fspathtree(context)['l2']) == ">>1 and inserted<<"



def test_expression_substitution():

  context = {'var1': "inserted", 'var3' : "==$(x/y)==", 'l2' : {'var1':1} }
  assert expression_substitution(">>$(var1)<<",context) == ">>$(var1)<<"
  assert expression_substitution(">>$(context['var1'])<<",context) == ">>inserted<<"

  assert expression_substitution(">>$(2 + 1)<<",context) == ">>3<<"
  assert expression_substitution("$(2 + 1) ",context) == "3 "
  assert expression_substitution("$(2 + 1)",context) == 3
  assert expression_substitution("$(abs(-2))",context) == 2
  assert expression_substitution("$(cos(60*pi/180))",context) == Approx(0.5)
  assert expression_substitution("$(sin(30*pi/180))",context) == Approx(0.5)

  context = {'x':1, 'y':2, 'z':3, 'l2' : {'x':11,'y':12,'z':13} }

  assert expression_substitution("$( context['x']+ context['y'] )", context) == 3
  assert expression_substitution("$( context['x']+ context['y'] ) ", context) == "3 "
  assert expression_substitution("$( ${x} + ${y} )", context) == "$( ${x} + ${y} )"
  assert expression_substitution("$( ${x} + ${y} )", context, expand_variables = True) == 3
  assert expression_substitution(" $( ${x} + ${y} )", context, expand_variables = True) == " 3"


def test_nested_expression_substitution():
  context = {'var1' : 1, 'var2' : 2}
  assert expression_substitution("$(1 + $(1 + 2))",context) == 4

  assert expression_substitution("$(1 + 1)",context) == 2
  assert expression_substitution("$($(1 + 1) + 1)",context) == 3
  assert expression_substitution("$($($(1 + 1) + 1) + 1)",context) == 4
  assert expression_substitution("$($($($(1 + 1) + 1) + 1) + 1)",context) == 5


def test_expression_with_filters_substitution():
  text = "$(10 |> str)"
  assert expression_substitution(text,{}) == "10"
  text = "$('10 ' |> int)"
  assert expression_substitution(text,{}) == 10

  text = "$(10 |> str)"
  assert expression_substitution(text,{},filters={'str':int}) == 10

  with pytest.raises(UnknownFilter):
    text = "$('10 ' |> unknown)"
    expression_substitution(text,{})






