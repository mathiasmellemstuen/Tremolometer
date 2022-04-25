import numpy as np
import scipy
import pywt


def wavelet_denoise(data, wavelet, noise_sigma):
    wavelet = pywt.Wavelet(wavelet)
    levels = min(15, (np.floor(np.log2(data.shape[0]))).astype(int))

    # Francisco's code used wavedec2 for image data
    wavelet_coeffs = pywt.wavedec(data, wavelet, level=levels)
    threshold = noise_sigma * np.sqrt(2 * np.log2(data.size))

    new_wavelet_coeffs = map(lambda x: pywt.threshold(x, threshold, mode='soft'),
                             wavelet_coeffs)

    return pywt.waverec(list(new_wavelet_coeffs), wavelet)
