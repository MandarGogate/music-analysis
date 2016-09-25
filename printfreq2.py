# Import the required functions
from scipy.io.wavfile import read
from scipy.fftpack import fft, fftfreq, fftshift
from scipy.signal import get_window
from math import ceil
from pylab import figure, imshow, clf, gray, xlabel, ylabel
import numpy as np
# Read in a wav file 
#   returns sample rate (samples / sec) and data
rate, data = read('nto2.wav')
print type(data)
print data.shape
# Define the sample spacing and window size.
dT = 1.0/rate
T_window = 50e-3
N_window = int(T_window * rate)
N_data = len(data)

# 1. Get the window profile
window = get_window('hamming', N_window)

# 2. Set up the FFT
result = []
start = 0
while (start < N_data - N_window):
    end = start + N_window
    print data[start:end].shape
    print data[start:end][0:]
    result.append(fftshift(fft(window*data[:,1][0:1102])))
    start = end

result.append(fftshift(fft(window*data[-N_window:,1])))
result = np.array(result,result[0].dtype)
print result
# Display results
freqscale = fftshift(fftfreq(N_window,dT))[150:-150]/1e3
figure(1)
clf()
imshow(abs(result[:,150:-150]),extent=(freqscale[-1],freqscale[0],(N_data*dT-T_window/2.0),T_window/2.0))
xlabel('Frequency (kHz)')
ylabel('Time (sec.)')
gray()