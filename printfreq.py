# Read in a WAV and find the freq's
import pyaudio
import wave
import numpy as np

chunk = 4048

#from pydub import AudioSegment
#song = AudioSegment.from_mp3("nto.mp3")
#song.export("nto.wav", format="wav")  # Is the same as:

# open up a wave
wf = wave.open('nto2.wav', 'rb')
swidth = wf.getsampwidth()
RATE = wf.getframerate()
# use a Blackman window
window = np.blackman(chunk)
# open stream
p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()), channels = wf.getnchannels(),
                rate = RATE,
                output = True)
# read some data
#data = wf.readframes(chunk)
data = wf.readframes(chunk)
#while len(data) > 0:
#    stream.write(data)
#    data = wf.readframes(chunk)
# play stream and find the frequency of each chunk
while len(data) == chunk*swidth:
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),data[0]))*window
    print indata
    # Take the fft and square each value
    fftData=abs(np.fft.rfft(indata))**2
    print fftData
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/chunk
        print "The freq is %f Hz." % (thefreq)
    else:
        thefreq = which*RATE/chunk
        print "The freq is %f Hz." % (thefreq)
    # read some more data
    data = wf.readframes(chunk)
print len(data)
print swidth
print chunk

if data:
    stream.write(data)
stream.close()
p.terminate()