from matplotlib import pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy import signal
import numpy as np

from typing import List
from costumeTyping import Data, Config


def calculate_average_spectrogram_data(Sxx, frequencies):
    mask = np.logical_and(frequencies >= 0, frequencies <=20)
    average_frequency = Sxx[mask].mean()
    print(average_frequency)

def create_spectrogram_from_data(data: List[Data], graph: Figure, config: Config, cmap_color: str) -> None:
    """!
    Create spectrogram figure for the GUI based on the Data measured.

    @param data Measurement data.
    @param graph The given matplotlib figure to use as a spectrogram.
    @param config Configuration dict
    """

    data_points = np.asarray(data)
    sampling_rate = 1 / 0.025
    frequencies, time, Sxx = signal.spectrogram(x=data_points, fs=sampling_rate, scaling="spectrum", mode="magnitude", nperseg=40, nfft=256)
    measuring_time = int(config["maaletid"] / 1000)

    row_sums = [sum(row) for row in Sxx]
    max_sum_index = row_sums.index(max(row_sums))

    print((20/len(row_sums)) * max_sum_index)

    frequencies_min = 0
    frequencies_max = 20

    graph.set_ylim(frequencies_min, frequencies_max)
    graph.set_yticks((list(range(frequencies_min, frequencies_max + 1))))
    graph.set_xlim(0, measuring_time)
    graph.set_xticks((list(range(0, measuring_time + 1))))
    graph.pcolormesh(time, frequencies,Sxx, antialiased=False, cmap=cmap_color)
