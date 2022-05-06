import json
import math
from os import path
from typing import List

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# from pprint import pprint


'''
I came up with a method, not sure if it does exactly what you are hoping but for your first dataset it is very close.
Basically I'm looking at the power spectral density of the power spectral density of your .wav files and sorting by the
normalized integral of that. (I have no good signal processing reason for doing this.
The PSD gives you an idea of how much energy is at each frequency.
I initially tried sorting by the PSD and got bad results.
Thinking that as you treat the files you were creating more variability,
I thought that would alter variation in the spectral density in this way and just tried it.)
If this does what you need, I hope you can find a justification for the approach.
'''


class Spec:
    name: str = ''
    sr: int = 44100


class MFCC(Spec):
    '''Step 1: This is pretty straightforward, just change y to self.y to add it to your MFCC class:'''
    mfcc: np.ndarray  # Mel-frequency cepstral coefficient
    delta_mfcc: np.ndarray  # delta Mel-frequency cepstral coefficient
    delta2_mfcc: np.ndarray  # delta2 Mel-frequency cepstral coefficient
    n_mfcc: int = 13

    def __init__(self, sound_file: str):
        self.name = path.basename(sound_file)
        self.y, sr = librosa.load(sound_file, sr=self.sr)  # <--- This line is changed
        self.mfcc = librosa.feature.mfcc(self.y, n_mfcc=self.n_mfcc, sr=sr)
        self.delta_mfcc = librosa.feature.delta(self.mfcc, mode="nearest")
        self.delta2_mfcc = librosa.feature.delta(self.mfcc, mode="nearest", order=2)


def get_mfccs(sound_files: List[str]) -> List[MFCC]:
    '''
    :param sound_files: Each item is a path to a sound file (wav, mp3, ...)
    '''
    mfccs = [MFCC(sound_file) for sound_file in sound_files]
    return mfccs


def draw_specs(spec_list: List[Spec], attribute: str, title: str):
    '''Takes a list of same type audio features, and draws a spectrogram for each one'''
    def draw_spec(spec: Spec, attribute: str, fig: plt.Figure, ax: plt.Axes):
        img = librosa.display.specshow(
            librosa.amplitude_to_db(getattr(spec, attribute), ref=np.max),
            y_axis='log',
            x_axis='time',
            ax=ax
        )
        ax.set_title(title + str(spec.name))
        fig.colorbar(img, ax=ax, format="%+2.0f dB")

    spec_len = len(spec_list)
    fig, axs = plt.subplots(math.ceil(spec_len/3), 3, figsize=(30, spec_len * 2))
    for spec in range(0, len(spec_list), 3):

        draw_spec(spec_list[spec], attribute, fig, axs.flat[spec])

        if (spec+1 < len(spec_list)):
            draw_spec(spec_list[spec+1], attribute, fig, axs.flat[spec+1])

        if (spec+2 < len(spec_list)):
            draw_spec(spec_list[spec+2], attribute, fig, axs.flat[spec+2])


def spectra_of_spectra(mfcc):
    '''
    Step 2: Calculate the PSD of the PSD and integrate (or really just sum):
    Dividing by the length (normalizing) helps to compare different files of different lengths.
    '''
    # first calculate the psd
    fft = np.fft.fft(mfcc.y)
    fft = fft[:len(fft)//2+1]
    psd1 = np.real(fft * np.conj(fft))
    # then calculate the psd of the psd
    fft = np.fft.fft(psd1/sum(psd1))
    fft = fft[:len(fft)//2+1]
    psd = np.real(fft * np.conj(fft))
    return(np.sum(psd)/len(psd))


def sort_mfccs(mfccs):
    values = [spectra_of_spectra(mfcc) for mfcc in mfccs]
    sorted_order = [i[0] for i in sorted(enumerate(values), key=lambda x:x[1], reverse=True)]
    return([mfccs[i] for i in sorted_order])


sound_files_1 = json.load(open('./data/sound_files_1.json'))
mfccs_1 = get_mfccs(sound_files_1)
spectra_of_spectra(mfccs_1[0])
sorted_mfccs_1 = sort_mfccs(mfccs_1)
draw_specs(sorted_mfccs_1, 'mfcc', 'spectra_of_spectra_transients_1 - ')
plt.savefig('spectra_of_spectra_transients_1.png')

sound_files_2 = json.load(open('./data/sound_files_2.json'))
mfccs_2 = get_mfccs(sound_files_2)
sorted_mfccs_2 = sort_mfccs(mfccs_2)
draw_specs(sorted_mfccs_2, 'mfcc', 'spectra_of_spectra_transients_2 - ')
plt.savefig('spectra_of_spectra_transients_2.png')

'''
Last point regarding question in code re: UserWarning

I am not familiar with the module you are using here,
but it looks like it is trying to do a FFT with a window length of 2048 on a file of length 1536.
FFTs are a building block of any sort of frequency analysis.
In your line self.mfcc = librosa.feature.mfcc(self.y, n_mfcc=self.n_mfcc, sr=sr)
you can specify the kwarg n_fft to remove this, for example, n_fft = 1024.
However, I am not sure why librosa uses 2048 as a default so you may want to examine closely before changing.
'''
