import pydantic


class DiscretizedInterval(pydantic.BaseModel):
  min: float
  max: float
  N: int

  @pydantic.validator('max')
  def max_must_be_greater_than_min(cls,v,values):
    if v <= values['min']:
      raise ValueError("'max' must be greater than 'min'.")
    return v

  @pydantic.validator('N')
  def N_must_be_two_or_more(cls,v):
    if v < 2:
      raise ValueError("'N' must be greater than one.")
    return v

class XYGrid(pydantic.BaseModel):
  x : DiscretizedInterval
  y : DiscretizedInterval

class XYZGrid(pydantic.BaseModel):
  x : DiscretizedInterval
  y : DiscretizedInterval
  z : DiscretizedInterval

class RZGrid(pydantic.BaseModel):
  r : DiscretizedInterval
  z : DiscretizedInterval
