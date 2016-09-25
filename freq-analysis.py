
#ederwander
#date 10/02/2012
from __future__ import division
import math
import wave
import numpy as np


freq = 0.;
trigfact = 0.6;
index1=100;
blockSize=4096;
spf = wave.open('test.wav','r');
fs = spf.getframerate();
signal = spf.readframes(-1);
signal = np.fromstring(signal, 'Int16');




index2=index1+blockSize-1;
schmittBuffer=signal[index1:int(index2)+1]



A1 = 0;
A2 = 0;

for j in range(0,blockSize):
	if (schmittBuffer[j]>0) and (A1<schmittBuffer[j]):
		A1 = schmittBuffer[j];
	if (schmittBuffer[j]<0) and (A2<-schmittBuffer[j]):
		A2 = -schmittBuffer[j];

t1 =   int( A1 * trigfact + 0.5);
t2 = - int( A2 * trigfact + 0.5);



startpoint=0;
j=1;
while((schmittBuffer[j]<=t1) and (j<blockSize-1)):
	
	j=j+1;
#print j

while (~(schmittBuffer[j-1]  >=t2 and schmittBuffer[j]< t2) and j<blockSize-2):
	#print j
	j=j+1;
	
startpoint=j;
schmittTriggered=0;
endpoint=startpoint+1;
tc=0;
for j in range(startpoint,blockSize-1):
	if (~schmittTriggered):
		schmittTriggered = (schmittBuffer[j] >= t1);
	else:
		if (schmittBuffer[j]>=t2 and schmittBuffer[j+1]<t2):
				endpoint=j;
				tc=tc+1;
        			schmittTriggered = 0;
if (endpoint > startpoint):
		freq = float(fs)*float(tc/(endpoint-startpoint));
print freq;