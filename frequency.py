import scipy
import scipy.fftpack
import pylab
from scipy import pi
import numpy as np
import scikits.audiolab
from scipy.io.wavfile import read


t = scipy.linspace(0,120,1000)
print t.shape
while 1:
    acc = lambda t: 10*scipy.sin(2*pi*2.0*t) + 5*scipy.sin(2*pi*8.0*t) + 2*scipy.random.random(len(t))
    
    signal = acc(t)
    print signal
    # open up a wave
    rate, data = read('nto2.wav')
    print type(data)
    print data
    print rate
    #signal = data.tolist()
    
    x, fs, nbits = scikits.audiolab.wavread("nto2.wav")
    X = scipy.fft(x)
    for i in range(4000,6000):
        print x[i],fs
    print fs
    print nbits
    import pylab
    print len(X)
    Xdb = 20*scipy.log10(scipy.absolute(X[:,0]))


    #Xdb = 20*scipy.log10(scipy.absolute(X[:,0]))
    f = scipy.linspace(0, fs, len(Xdb))
    signal =f[0:len(signal)]
    
    FFT = abs(scipy.fft(signal))
    freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
    #freqs = scipy.fftpack.fftfreq(len(signal), d=1.0)
    print freqs
    pylab.subplot(211)
    
    pylab.plot(t, signal)
    pylab.subplot(212)
    pylab.plot(freqs,20*scipy.log10(FFT),'x')
    pylab.show()
    exit()
