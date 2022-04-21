from matplotlib import pyplot as plot
from scipy import signal
import numpy as np


def create_spectrogram_from_data(data, graph, config):
    data_points = []
    for i in data:
        data_points.append(i[1])

    data_points = np.asarray(data_points)
    sampling_rate = 1/0.005
    segment_length = 100
    frequencies, time, Sxx = signal.spectrogram(x=data_points, fs=10 * sampling_rate, mode="psd", scaling="density", nperseg=segment_length, nfft=None, noverlap=10)

    frequencies_min = 0
    frequencies_max = 20
    print(frequencies)
    print(time)
    print(Sxx)
    frequencies_slice = np.where((frequencies >= frequencies_min) & (frequencies <= frequencies_max))
    frequencies = frequencies[frequencies_slice]
    Sxx = Sxx[frequencies_slice, :][0]

    measuring_time = int(config["maaletid"] / 1000)

    graph.set_ylim(frequencies_min, frequencies_max)
    graph.set_yticks((list(range(frequencies_min, frequencies_max + 1))))
    graph.set_xlim(0, measuring_time)
    graph.set_xticks((list(range(0, measuring_time + 1))))
    graph.pcolormesh(time, frequencies, Sxx, antialiased=True, cmap="hot")
