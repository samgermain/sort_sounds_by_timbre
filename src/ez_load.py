from typing import Optional
import librosa


def ez_load(sound_file: str, sr: Optional[int] = None):
    if sr:
        y, sr = librosa.load(sound_file, sr=sr)
    else:
        y, sr = librosa.load(sound_file)
    return y, sr
