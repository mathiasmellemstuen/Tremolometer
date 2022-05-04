"""!
Functions related to plotting, creating and modifying spectrograms.
"""
from scipy import signal
from typing import List, Any
from customTypes import Data, Config
from graphData import GraphData

import numpy as np


def calculate_strongest_spectrogram_frequency(spectrogram: np.ndarray, frequencies_max: int) -> float:
    """!
    Using the data from a spectrogram to calculate the strongest frequency from the spectrogram.

    @param spectrogram 2D-array of values inside the spectrogram.
    @param frequencies_max The max frequency of the spectrogram.
    @return Returns the strongest frequency in the provided spectrogram
    """
    row_sums = [sum(row) for row in spectrogram]
    max_sum_index = row_sums.index(max(row_sums))
    return (frequencies_max * max_sum_index) / len(row_sums)


def mask_spectrogram(spectrogram: np.ndarray, mask_percentage: int) -> np.ndarray:
    """!
    Masking out lower values of a spectrogram.

    @param spectrogram 2D-array of values inside the spectrogram
    @param mask_percentage Value between 0-1. Percentage of the range of values that will be excluded
    @return Returns a new 2D-array spectrogram with the lower values masked.
    """
    max_value = np.amax(spectrogram)

    for i in range(len(spectrogram) - 1):
        for j in range(len(spectrogram[i]) - 1):
            if spectrogram[i][j] / max_value < mask_percentage:
                spectrogram[i][j] = 0
    return spectrogram


def create_spectrogram_from_data(data: List[Data], figure: Any, config: Config, cmap_color="hot") -> float:
    """!
    Create spectrogram figure for the GUI based on the Data measured.

    @param data List of data to include in the spectrogram. One dimentional data
    @param figure The matplotlib figure to draw the spectrogram on.
    @param config Configuration from the configuration file (config.yaml)
    @param cmap_color Colormap type of the spectrogram.
    @return Returns the strongest frequency in the spectrogram
    """
    data_points = np.asarray(data)
    sampling_rate = 1 / 0.025
    frequencies, time, spectrogram = signal.spectrogram(x=data_points, fs=sampling_rate, scaling="spectrum",
                                                        mode="magnitude", nperseg=40, nfft=256)

    measuring_time = int(config["maaletid"])
    frequencies_min = int(config["frekvens_min"])
    frequencies_max = int(config["frekvens_maks"])
    mask_percentage = int(config["spektrogram_maske"])

    frequencies, time, spectrogram = signal.spectrogram(data_points, sampling_rate,
                                                        scaling="spectrum", mode="magnitude",
                                                        **dict(config['spectogram_grid_style']))

    # Masking the spectrogram to remove lower unwanted values
    spectrogram = mask_spectrogram(spectrogram=spectrogram, mask_percentage=mask_percentage)

    figure.set_ylim(frequencies_min, frequencies_max)
    figure.set_yticks((list(range(frequencies_min, frequencies_max + 1))))
    figure.set_xlim(0, measuring_time)
    figure.set_xticks((list(range(0, measuring_time + 1))))
    figure.pcolormesh(time, frequencies, spectrogram, antialiased=False, cmap=cmap_color)
    figure.axes.grid(**GraphData.grid_style)

    return calculate_strongest_spectrogram_frequency(spectrogram, frequencies_max)