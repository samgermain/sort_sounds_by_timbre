import librosa
import numpy as np


class Spec:
    name: str = ''
    sr: int = 44100


class MFCC(Spec):
    mfcc: np.ndarray  # Mel-frequency cepstral coefficient
    delta_mfcc: np.ndarray  # delta Mel-frequency cepstral coefficient
    delta2_mfcc: np.ndarray  # delta2 Mel-frequency cepstral coefficient
    n_mfcc: int = 13

    def __init__(self, index: int, sound_file: np.ndarray, sr: int = 44100):
        self.name = str(index)
        self.mfcc = librosa.feature.mfcc(sound_file, n_mfcc=self.n_mfcc, sr=sr)
        self.delta_mfcc = librosa.feature.delta(self.mfcc, mode="nearest")
        self.delta2_mfcc = librosa.feature.delta(
            self.mfcc,
            mode="nearest",
            order=2
        )
