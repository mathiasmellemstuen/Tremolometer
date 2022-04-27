from matplotlib.figure import Figure
from scipy import signal
from typing import List, Any
from customTypes import Data, Config

import numpy as np


def calculate_strongest_spectrogram_frequency(Sxx, frequencies_max):
    row_sums = [sum(row) for row in Sxx]
    max_sum_index = row_sums.index(max(row_sums))
    return (frequencies_max * max_sum_index) / len(row_sums)


def mask_spectrogram(Sxx, mask_percentage):
    max_value = np.amax(Sxx)

    for i in range(len(Sxx) - 1):
        for j in range(len(Sxx[i]) - 1):
            if Sxx[i][j] / max_value < mask_percentage:
                Sxx[i][j] = 0
    return Sxx


def create_spectrogram_from_data(data: List[Data], figure: Figure, config: Config, cmap_color="hot") -> Any:
    """!
    Create spectrogram figure for the GUI based on the Data measured.

    @param data Measurement data.
    @param figure The given matplotlib figure to use as a spectrogram.
    @param config Configuration dict
    """

    data_points = np.asarray(data)
    sampling_rate = 1 / 0.025
    frequencies, time, Sxx = signal.spectrogram(x=data_points, fs=sampling_rate, scaling="spectrum", mode="magnitude",
                                                nperseg=40, nfft=256)

    measuring_time = int(config["maaletid"])
    frequencies_min = int(config["frekvens_min"])
    frequencies_max = int(config["frekvens_maks"])
    mask_percentage = int(config["spektrogram_maske"])

    # Masking the spectrogram to remove lower unwanted values
    Sxx = mask_spectrogram(Sxx, mask_percentage=mask_percentage)

    figure.set_ylim(frequencies_min, frequencies_max)
    figure.set_yticks((list(range(frequencies_min, frequencies_max + 1))))
    figure.set_xlim(0, measuring_time)
    figure.set_xticks((list(range(0, measuring_time + 1))))
    figure.pcolormesh(time, frequencies, Sxx, antialiased=False, cmap=cmap_color)
    figure.axes.grid(color='white', linestyle='dashed')

    return calculate_strongest_spectrogram_frequency(Sxx, frequencies_max)
