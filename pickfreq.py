import scipy, pylab
import wave
import struct
import sys

def stft(data, cp, do, hop):
    dos = int(do*cp)
    w = scipy.kaiser(dos,12) 
    temp=[]
    wyn=[]
    for i in range(0, len(data)-dos, hop):
        temp=scipy.fft(w*data[i:i+dos])
        max=-1
        for j in range(0, len(temp),1):
            licz=temp[j].real**2+temp[j].imag**2
            if( licz>max ):
                max = licz
                maxj = j
        wyn.append(maxj)
    #wyn = scipy.array([scipy.fft(w*data[i:i+dos])
        #for i in range(0, len(data)-dos, 1)])
    return wyn

#file = wave.open(sys.argv[1])
file = wave.open('nto2.wav')
bity = file.readframes(file.getnframes())
data=struct.unpack('{n}h'.format(n=file.getnframes()), bity)
file.close()

cp=44100 #sampling frequency
do=5 #window size
hop = 5

wyn=stft(data,cp,do,hop)
print len(wyn)
for i in range(0, len(wyn), 1):
    print i
    print wyn[i]