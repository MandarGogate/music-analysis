import numpy as np
#http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/   .....to paradeigma vrethike edw


def speedx(sound_array, factor):
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int) ]
		
def stretch(sound_array, f, window_size, h):
    """ Stretches the sound by a factor `f` """

    phase  = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros( len(sound_array) /f + window_size)

    for i in np.arange(0, len(sound_array)-(window_size+h), h*f):

        # two potentially overlapping subarrays
        a1 = sound_array[i: i + window_size]
        a2 = sound_array[i + h: i + window_size + h]

        # resynchronize the second array on the first
        s1 =  np.fft.fft(hanning_window * a1)
        s2 =  np.fft.fft(hanning_window * a2)
        phase = (phase + np.angle(s2/s1)) % 2*np.pi
        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))

        # add to result
        i2 = int(i/f)
        result[i2 : i2 + window_size] += hanning_window*a2_rephased

    result = ((2**(16-4)) * result/result.max()) # normalize (16bit)

    return result.astype('int16')

def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)

 
from scipy.io import wavfile

fps, bowl_sound = wavfile.read("La-note.wav")
tones = range(-25,25)
transposed = [pitchshift(bowl_sound[a[0,], n) for n in tones]



import pygame

pygame.mixer.init(fps, -16, 1, 512) # so flexible ;)
screen = pygame.display.set_mode((640,480)) # for the focus

# Get a list of the order of the keys of the keyboard in right order.
# ``keys`` is like ['Q','W','E','R' ...] 
keys = open('typewriter.kb').read().split('\n')

sounds = map(pygame.sndarray.make_sound, transposed)
key_sound = dict( zip(keys, sounds) )
is_playing = {k: False for k in keys}

while True:

    event =  pygame.event.wait()

    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        key = pygame.key.name(event.key)

    if event.type == pygame.KEYDOWN:

        if (key in key_sound.keys()) and (not is_playing[key]):
            key_sound[key].play(fade_ms=50)
            is_playing[key] = True

        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            raise KeyboardInterrupt

    elif event.type == pygame.KEYUP and key in key_sound.keys():

        key_sound[key].fadeout(50) # stops with 50ms fadeout
        is_playing[key] = False


