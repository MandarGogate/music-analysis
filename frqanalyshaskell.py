from pylab import plot, show, title, xlabel, ylabel, subplot, savefig
from scipy import fft, arange, ifft
from numpy import sin, linspace, pi
import math as Math
from scipy.io.wavfile import read,write

def plotSpectru(y,Fs):
 n = len(y) # lungime semnal
 k = arange(n)
 T = n/Fs
 frq = k/T # two sides frequency range
 frq = frq[range(n/2)] # one side frequency range
 
 Y = fft(y)/n # fft computing and normalization
 Y = Y[range(n/2)]
 
 plot(frq,abs(Y),'r') # plotting the spectrum
 xlabel('Freq (Hz)')
 ylabel('|Y(freq)|')
 return frq,Y,T
Fs = 44100;  # sampling rate

rate,data=read('nto2.wav')
y=data[:,1]
lungime=len(y)
timp=len(y)/44100.
t=linspace(0,timp,len(y))

subplot(2,1,1)
plot(t,y)
xlabel('Time')
ylabel('Amplitude')
subplot(2,1,2)
frq,Y,T = plotSpectru(y,Fs)
#frq,Y,T = plotSpectru(y,rate)
print abs(Y)
print 'frq:','--',frq[2]
i=0
for x in abs(Y):
    temp=abs(Y[i])
    if temp>abs(Y[i]):
        max = temp
    else:
        max = abs(Y[i])
    i+=1
print max
show()