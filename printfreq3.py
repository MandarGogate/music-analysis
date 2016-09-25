import scikits.audiolab, scipy
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

pylab.plot(f, Xdb)
pylab.show()