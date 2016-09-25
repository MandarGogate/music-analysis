scipy.io.wavfile.read(filename, mmap=False)[source]
Return the sample rate (in samples/sec) and data from a WAV file

Parameters:	
filename : string or open file handle
Input wav file.
mmap : bool, optional
Whether to read data as memory mapped. Only to be used on real files (Default: False)
New in version 0.12.0.
Returns:	
rate : int
Sample rate of wav file
data : numpy array
Data read from wav file


