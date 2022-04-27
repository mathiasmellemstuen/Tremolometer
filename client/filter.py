from scipy.signal import butter, lfilter


def butter_lowpass(cut_off, fs, order=5):
    """!
    Noe her

    @params cut_off
    @params fs
    @params order
    """
    return butter(order, cut_off, fs=fs, btype='low', analog=False)


def low_pass_filter(data, cut_off, fs, order=4):
    """!
    Noe her

    @params data
    @params cut_off
    @params fs
    @params order
    """
    b, a = butter_lowpass(cut_off, fs, order=order)
    return lfilter(b, a, data)
