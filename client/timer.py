"""!
Contains functions for timekeeping and conversion between time units.
"""
import time


def get_current_time_ms() -> int:
    """!
    Calculates the time in milliseconds.

    @return Time in milliseconds
    """
    return round(time.time() * 1000)
