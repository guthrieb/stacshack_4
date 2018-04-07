from __future__ import print_function
import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
import numpy as np
import math
from matplotlib import pyplot as plt

import socket

UDP_IP = "192.168.122.1"
UDP_PORT = 12340
MESSAGE = "Hello, World!"

MCAST_GRP = '192.168.122.1'
MCAST_PORT = 5007

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    while(True):
        sock.sendto(MESSAGE.encode(), (MCAST_GRP, MCAST_PORT))
    # handle_file("test_files/test_high_pitch.wav", 20000)

def handle_file(filename, time_sample_dif, multichannel=False):
    fs_rate, signal = wavfile.read(filename)

    #Combine channels
    if not multichannel:
        n_channels = len(signal.shape)
        if n_channels > 1:
            signal = signal.sum(axis=1) / n_channels
        total_samples = signal.shape[0]

    return get_magnitudes(fs_rate, signal, total_samples, time_sample_dif)

def get_magnitudes(fs_rate, waveform, total_samples, time_sample_dif):
    n_measurements = (total_samples + time_sample_dif // 2) // time_sample_dif

    #Length in seconds
    secs = total_samples / float(fs_rate)
    send_rate = float(fs_rate)/100

    #Sample period
    Ts = 1.0/fs_rate
    time = scipy.arange(0, secs/n_measurements, Ts)

    results = []
    for index in range(0, n_measurements):
        start_index = index*time_sample_dif
        end_index = start_index + time_sample_dif

        if(end_index < total_samples):
            end_index = total_samples

        print("Measuring")
        print(start_index)
        print(end_index)
        print(time_sample_dif)
        results.append(fft_section_of_waveform(fs_rate,
        waveform[start_index:end_index], time, time_sample_dif))

def fft_section_of_waveform(fs_rate, waveform, time, n_samples):
    #Pad to nearest value of 2
    #Not entirely necessary but significantly speeds up processing, creates noise however
    next = pow(2, math.ceil(math.log(len(waveform))/math.log(2)));
    waveform = np.array(waveform)
    waveform = np.pad(waveform, (0, next - len(waveform)), 'constant', constant_values=(0, 0))

    FFT = abs(scipy.fft(waveform))

    #Magnitudes
    FFT_side = abs(FFT[range(n_samples//2)])
    freqs = scipy.fftpack.fftfreq(waveform.size, time[1]-time[0])

    print(freqs)
    #Frequencies
    freqs_side = freqs[range(n_samples//2)]

    return (freqs_side, freqs)
    # #Plot FFT
    # plt.subplot(312)
    # p3 = plt.plot(freqs_side, FFT_side, "b")
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Count single-sided')
    # plt.show()

    
if __name__ == "__main__":
    main()
