import numpy as np
import matplotlib.pylab as plt
from numpy.fft import *
import pdb

def nextpow2(i):
    n = 2
    while n < i:
        n = n * 2
    return n

def gen_oct_fr(octType, fst, fed):
    """ generate oct or 1/3oct band frequencies
        gen_oct_fr(octType, fst, fed):
        octType:  'oct' or '1/3oct' as string
        fst:   start frequency
        fed:   end frequency
    """
    Lf, cf, rf = [], [], []
    if octType=='oct':
        start = round(np.log2(fst/1000))
        stop = round(np.log2(fed/1000))-1
        bands = np.linspace(start, stop, stop-start+1)
        for n in range(len(bands)):
            cf += [1000*(2)**bands[n]]
            Lf += [cf[n]/(2**(1/2))]
            rf += [cf[n]*(2**(1/2))]
    elif octType=='1/3oct':
        start = round(3*np.log2(fst/1000))
        stop = round(3*np.log2(fed/1000))-1
        bands = np.linspace(start, stop, stop-start+1)        
        for n in range(len(bands)):
            cf += [1000*(2**(1/3))**bands[n]]
            Lf += [cf[n]/(2**(1/6))]
            rf += [cf[n]*(2**(1/6))]
    else:
        print('choose oct, or 1/3oct')

    return [Lf, cf, rf]



t = np.loadtxt("xverloop1.txt")
print ("shape of signal: ", np.shape(t))
fs = np.abs(1/(t[0, 0]-t[1, 0]))
print ("fs: ", fs)
NT = nextpow2(len(t[:, 1]))
NFFTs = [NT, 2*NT, 4*NT]

cmp = []
for NFFT in NFFTs:
    yfft = fft(t[:, 1], NFFT)
    freq = np.linspace(1, NFFT, NFFT)/NFFT*fs
    df = freq[1]-freq[0]
    print ("df: ", df, " max freq: ", max(freq))

    [Lf, cf, rf] = gen_oct_fr("1/3oct", 25, 2500)
    yabs = np.abs(yfft)  # amplitude array
    spl = []
    for n in range(len(cf)):
        start = round(Lf[n]/df)
        stop = round(rf[n]/df)
        spl += [20*np.log10(np.sqrt(1/NFFT*sum(yabs[start:stop]**2)))]
    cmp.append(spl)

plt.plot(cf, cmp[0], cf, cmp[1], cf, cmp[2])
plt.legend(["NFFT", "2*NFFT", "4*NFFT"])
plt.show()

print("\n")
total = 20*np.log10(1/NFFT*np.sqrt(sum(yabs**2)))
totalf = 10*np.log10(1/NFFT*2*sum(10**(0.1*np.array(spl)))) # double the energy

print ("total value is: ", total)
print ("come from f: ", totalf)