"""!
Custom types used in codebase.
"""
from typing import TypeVar, Any, Tuple

## Define Config as a type
Config = TypeVar('Config', bound=Any)

## Define Data as type
Data = TypeVar('Data', bound=Tuple[int, int, int, int])

## Define Plot as type
Plot = TypeVar('Plot', bound=Any)

## Define Widget as type
Widget = TypeVar('Widget', bound=Any)
