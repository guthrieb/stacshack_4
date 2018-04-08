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

TIME_SAMPLE_DIFF = 1000

def main():
    handle_file("test_files/test.wav")

def handle_file(filename, multichannel=False):
    fs_rate, waveform = wavfile.read(filename)

    if not multichannel:
        n_channels = len(waveform.shape)
        if n_channels > 1:
            waveform = waveform.sum(axis=1) / n_channels
        total_samples = waveform.shape[0]

    print(len(waveform))
    print(total_samples)

    results = []
    for x in range(20000, total_samples, 20000):
        print("Calculating, ", x)
        res1 = get_frequencies_against_amplitudes(waveform[x-20000:x], fs_rate, 20000)

        frequencies = res1[0]
        amplitudes = res1[1]

        print(len(frequencies))

    return [results]

def get_frequencies_against_amplitudes(waveform, sampling_rate, number_of_samples, plotting=True):
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

    return (freqs_x, abs(ampt_y))


def pad_waveform(waveform):
    # Pad out sampled waveform to nearest power of two
    next = pow(2, math.ceil(math.log(len(waveform))/math.log(2)));
    waveform = np.array(waveform)
    waveform = np.pad(waveform, (0, next - len(waveform)), 'constant', constant_values=(0, 0))
    return waveform

if __name__ == "__main__":
    main()
