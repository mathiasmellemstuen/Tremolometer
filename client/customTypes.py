"""!
Custom types to use in the code
"""
from typing import TypeVar, Any, Tuple

Config = TypeVar('Config', bound=Any)
"""!Define Config as a type"""

Data = TypeVar('Data', bound=Tuple[int, int, int, int])
"""!Define Data as type"""

Plot = TypeVar('Plot', bound=Any)
"""!Define Plot as type"""

Widget = TypeVar('Widget', bound=Any)
