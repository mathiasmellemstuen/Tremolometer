"""!
Costume types to use in the code

@todo
    Add datatypes for plot and widget
"""
from typing import TypeVar, Any, Tuple

Config = TypeVar('Config', bound=Any)
"""!Define Config as a type"""

Data = TypeVar('Data', bound=Tuple[int, int, int, int])
"""!Define Data as type"""
