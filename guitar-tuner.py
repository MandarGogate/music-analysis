# Copyright (c) 2010, Eng Eder de Souza
#    ___    _              _       ___
#   | __|__| |___ _ _   __| |___  / __| ___ _  _ _____ _
#   | _|/ _` / -_) '_| / _` / -_) \__ \/ _ \ || |_ / _` |
#   |___\__,_\___|_|   \__,_\___| |___/\___/\_,_/__\__,_|
#Real Time Eletric Guitar tuner by Microphone or Input
#Guitar tuner using Average magnitude difference function-AMDF
#http://ederwander.wordpress.com/2011/09/09/experimental-guitar-tuner/
#Eng Eder de Souza
#date 23/08/2010


from __future__ import division
from matplotlib.mlab import find
import sys
import math
import wave
import pyaudio
import numpy as np

#const vars
ratio=5.0
min_frequency=82.0;
max_frequency=1000.0;
chunk=1024;
FORMAT=pyaudio.paInt16;
CHANNELS=1;
RATE=44100;
max_period = int(RATE / min_frequency + 0.5);
min_period = int(RATE / max_frequency + 0.5);
sens=0.1;


def AMDF(frame, maxShift):
	frameSize=len(frame);
 	amd=np.zeros(maxShift);
	for i in range(1,int(maxShift)):
		AuxFrame1=frame[0:(frameSize-i)]
		AuxFrame2=frame[i:frameSize]
		AuxFrame1=np.asarray(AuxFrame1);
		AuxFrame2=np.asarray(AuxFrame2);
		CalcSub=((AuxFrame1)-(AuxFrame2));
		amd[i]=sum(abs(CalcSub));
	return abs(amd);


def ComputeAMD(amd):
	amd2=amd[min_period:max_period]
	posmax = amd2.argmax();
	posmin = amd2.argmin();
	maxval = amd2[posmax];
	minval = amd2[posmin];
	offset = int(sens * float((maxval - minval))) + minval
	j=min_period;
	while((j<=max_period) & (amd[j] > offset)):
		j=j+1;
	search_length = min_period / 2;
	minval = amd[j];
	minpos = j;
	i=j;
	while((i<j+search_length) & (i<=max_period)):
		i=i+1;
		if(amd[i] < minval):
          		minval = amd[i];
          		minpos = i;
			return minpos;
		else:
			return None;
	

def lognote(freq):
	oct = (math.log(freq)-math.log(440))/math.log(2)+4.0; 
	return oct;


def freq_to_note(freq):
	lnote = lognote( freq ); 
	oct = math.floor( lnote ); 
	cents = 1200 * ( lnote - oct );
	offset = 50.0;
	x = 2;
	if ( cents < 50 ): 
		note = "A ";
	elif ( cents >= 1150 ):
		note = "A ";
		cents -= 1200;
		++oct;
	else:
		for  j in range(11):
			if (cents >= offset) and (cents < (offset + 100)):
				note = (Notes_Table[x] + Notes_Table[x+1]);
				cents -= ( j * 100 );
				break;
			offset += 100;
			x += 2;
	return note,oct;

Notes_Table= "A A#B C C#D D#E F F#G G#";
pyaud=pyaudio.PyAudio();
try:
	stream = pyaud.open(format = FORMAT,
		    channels          = CHANNELS,
		    rate              = RATE,
		    input             = True,
		    output            = True,
		    frames_per_buffer = chunk)
except:
	print "device not found"
	sys.exit()

print "Guitar Tuner";

while True:
	
	try:

		raw = stream.read(chunk);

	except:

		continue;
	
	signal = np.fromstring(raw, dtype=np.int16);
	maxShift=len(signal);
	amd=AMDF(signal,maxShift);
	minpos=ComputeAMD(amd);

	if minpos is not None:
		freq = RATE/(minpos);
		note,oct=freq_to_note(freq);
		noteValue= note + str(int(oct));
		sys.stdout.write("\rNote:...%s  Frequency:...%s" %(noteValue, int(freq)));
       	        sys.stdout.flush()