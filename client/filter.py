import numpy as np
from scipy.signal import butter, lfilter
from scipy.signal import freqs

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff=cutoff, fs=fs, order=order)
    y = lfilter(b, a, data)
    return y