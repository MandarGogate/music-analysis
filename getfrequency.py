import scipy
import scipy.fftpack
import pylab
from scipy import pi


t = scipy.linspace(10,20,500)
acc = lambda t: 10*scipy.sin(2*pi*440.0*t)
signal = acc(t)

FFT = abs(scipy.fft(signal))


freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])

print freqs.shape
print freqs[1:100]
print signal.shape 
print signal[1:100]


pylab.subplot(211)
pylab.plot(t, signal)
pylab.subplot(212)
pylab.plot(freqs,20*scipy.log10(FFT),'x')
pylab.show()