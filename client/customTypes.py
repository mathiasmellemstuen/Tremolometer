"""!
Custom types used in codebase.
"""
from typing import TypeVar, Any, Tuple, Union, Iterable

## Define Config as a type
from numpy import ndarray

Config = TypeVar('Config', bound=Any)

## Define Data as type
Data = TypeVar('Data', bound=Tuple[int, int, int, int])

## Define Plot as type
Plot = TypeVar('Plot', bound=Any)

## Define Widget as type
Widget = TypeVar('Widget', bound=Any)

## Define lfilter as type
lfilter = TypeVar('lfilter', bound=Union[ndarray, Iterable, int, float,
                                         tuple[Union[ndarray, Iterable, int, float],
                                               Union[ndarray, Iterable, int, float, None]
                                         ]])
