import stft
import aifc
import scipy.io.wavfile as wav

fs, audio = wav.read('nto2.wav')
specgram = stft.spectrogram(audio)
output = stft.ispectrogram(specgram)
wav.write('output.wav', fs, output)
print fs,audio