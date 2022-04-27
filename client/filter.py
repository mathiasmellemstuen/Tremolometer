"""!
Contains lowpass filter for a digital signal.
"""
from scipy.signal import butter, lfilter


def butter_lowpass(cut_off, fs, order=5):
    """!
    Creates filter coefficients from a butterworth digital filter design.

    @param cut_off the cutoff frequency of the lowpass filter
    @param fs The sampling frequency of the signal
    @param order The order of the filter

    @return Returning filter coefficients
    """
    return butter(order, cut_off, fs=fs, btype='low', analog=False)


def low_pass_filter(data, cut_off, fs, order=4):
    """!
    Filtering a digital signal with lowpass filter.

    @param data The signal
    @param cut_off The cutoff frequency of the lowpass filter.
    @param fs The sampling frequency of the signal
    @param order The order of the filter

    @return Returning filtered signal
    """
    b, a = butter_lowpass(cut_off, fs, order=order)
    return lfilter(b, a, data)
