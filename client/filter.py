import numpy as np
from scipy.signal import butter, lfilter

def butter_lowpass(cut_off, fs, order=5):
    return butter(order, cut_off, fs=fs, btype='low', analog = False)

def low_pass_filter(data, cut_off, fs, order=4):
    b, a = butter_lowpass(cut_off, fs, order=order)
    return lfilter(b, a, data)