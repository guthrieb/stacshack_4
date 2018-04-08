from __future__ import print_function
import scipy.io.wavfile as wavfile
import scipy
from scipy.fftpack import fft
import numpy as np
import math
from matplotlib import pyplot as plt
from operator import itemgetter

import socket
import json

def handle_file(filename, multichannel=True):
    fs_rate, waveform = wavfile.read(filename)
    time_sample_diff = int(round((fs_rate/60)))

    n_channels = len(waveform.shape)
    print(n_channels)
    if not multichannel:
        if n_channels > 1:
            waveform = waveform.sum(axis=1) / n_channels
            results = [calc_results_for_channel(waveform, fs_rate, time_sample_diff)]
            return results
    else:
        results = []
        for i in range(0, n_channels):
            channel = waveform[:,i]
            results.append(calc_results_for_channel(channel, fs_rate, time_sample_diff))
        return zip(*results)

def calc_results_for_channel(waveform, fs_rate, time_sample_diff):
    total_samples = waveform.shape[0]
    results = []
    for x in range(time_sample_diff, total_samples, time_sample_diff):
        res1 = get_frequencies_against_amplitudes(waveform[x-time_sample_diff:x], fs_rate, time_sample_diff)

        frequencies = res1[0]
        amplitudes = res1[1]

        results.append(amplitudes)

    return results

def get_frequencies_against_amplitudes(waveform, sampling_rate, number_of_samples, plotting=False):
    secs = number_of_samples / float(sampling_rate)
    sampling_period = 1.0/sampling_rate
    time_periods = scipy.arange(0, secs, sampling_period)

    #Pad waveform to nearest power of 2
    waveform = pad_waveform(waveform)

    #y-axis
    FFT = abs(scipy.fft(waveform))
    ampt_y = FFT[range(number_of_samples//2)]

    #X-axis
    freqs = scipy.fftpack.fftfreq(waveform.size, time_periods[1]-time_periods[0])
    freqs_x = freqs[range(number_of_samples//2)]

    if plotting:
        plt.subplot(313)
        p3 = plt.plot(freqs_x, abs(ampt_y), "b")
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Count single-sided')
        plt.show()

    return (freqs_x.tolist(), abs(ampt_y).tolist())


def pad_waveform(waveform):
    # Pad out sampled waveform to nearest power of two
    next = pow(2, math.ceil(math.log(len(waveform))/math.log(2)));
    waveform = np.array(waveform)
    waveform = np.pad(waveform, (0, next - len(waveform)), 'constant', constant_values=(0, 0))
    return waveform

if __name__ == "__main__":
    main()
