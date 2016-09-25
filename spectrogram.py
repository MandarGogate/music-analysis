import stft
import scipy.io.wavfile as wav

fs, audio = wav.read('nto2.wav','r')
specgram = stft.spectrogram(audio)
output = stft.ispectrogram(specgram)
print output