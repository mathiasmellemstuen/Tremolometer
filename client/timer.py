"""!
@package Timer
Different time functions.
"""
import time


def get_current_time_ms() -> int:
    """!
    Return the rounded time.

    @return Time rounded
    """
    return round(time.time() * 1000)
