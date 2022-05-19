"""!
Contains lowpass filter for a digital signal.
"""
from typing import Optional, Any, List
from customTypes import lfilter

from scipy.signal import butter, lfilter


def butter_lowpass(cut_off: float, fs: Optional[float], order=5) -> Any:
    """!
    Creates filter coefficients from a butterworth digital filter design.

    @param cut_off the cutoff frequency of the lowpass filter
    @param fs The sampling frequency of the signal
    @param order The order of the filter

    @return Returning filter coefficients
    """
    return butter(order, cut_off, fs=fs, btype='low', analog=False)


def low_pass_filter(data: List[int], cut_off: float, fs: Optional[float], order=5) -> lfilter:
    """!
    Filtering a digital signal with lowpass filter.

    @param data The signal
    @param cut_off The cutoff frequency of the lowpass filter.
    @param fs The sampling frequency of the signal
    @param order The order of the filter

    @return Returning filtered signal
    """
    b, a = butter_lowpass(cut_off, fs, order)
    return lfilter(b, a, data)
