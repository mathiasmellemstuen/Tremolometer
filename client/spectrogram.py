from matplotlib import pyplot as plot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy import signal
import numpy as np

from typing import List
from costumeTyping import Data, Config


def create_spectrogram_from_data(data: List[Data], graph: Figure, config: Config) -> None:
    """!
    Create spectrogram figure for the GUI based on the Data measured.

    @param data Measurement data.
    @param graph The given matplotlib figure to use as a spectrogram.
    @param config Configuration dict
    """
    data_points = []
    for i in data:
        data_points.append(i[1])

    data_points = np.asarray(data_points)
    sampling_rate = 1/0.003
    segment_length = 200
    frequencies, time, Sxx = signal.spectrogram(x=data_points, fs=sampling_rate, mode="psd", scaling="density", nperseg=segment_length, nfft=100*segment_length, window=("tukey", 0.25), noverlap=100)
    measuring_time = int(config["maaletid"] / 1000)

    frequencies_min = 0
    frequencies_max = 20
    graph.set_ylim(frequencies_min, frequencies_max)
    graph.set_yticks((list(range(frequencies_min, frequencies_max + 1))))
    graph.set_xlim(0, measuring_time)
    graph.set_xticks((list(range(0, measuring_time + 1))))
    graph.pcolormesh(time, frequencies, 10 * Sxx, antialiased=True, cmap="inferno")