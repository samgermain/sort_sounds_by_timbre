# import matplotlib.pyplot as plt
import librosa
import numpy as np
import os
import soundfile as sf
import pretty_midi
import shutil

from typing import List, Optional
# from config import assets


def getOnsetsFromMidi(midiFile, sr: int):
    midiData = pretty_midi.PrettyMIDI(midiFile)
    onsets = midiData.get_onsets()
    arr = np.array(onsets)
    return librosa.core.time_to_samples(times=arr, sr=sr)


def getOnsets(y: np.ndarray, sr: int):
    C = np.abs(librosa.cqt(y=y, sr=sr))
    oEnv = librosa.onset.onset_strength(sr=sr, S=librosa.amplitude_to_db(C, ref=np.max))
    onsets = librosa.onset.onset_detect(onset_envelope=oEnv, sr=sr)
    return librosa.frames_to_samples(onsets)


def onsetsToTransientLocations(onsetSamples: List[int]):
    """Takes a list of onset times for an audio file and returns the list of start and stop times for that audio file
    :param [int] onset_samples: I don't really know what these are actually.
        I thought they were start times for each sound change but I don't know
    :return [(int, int)]: A list of start and stop times for each sound change
    """

    starts = onsetSamples[0:-1]
    stops = onsetSamples[1:]
    transientTimes = []
    for s in range(len(starts)):
        transientTimes.append([starts[s], stops[s]])
    return np.array(transientTimes)


def locationsToSamples(y: np.ndarray, transientLocations):
    transientSamples = []

    for time in transientLocations:
        transientSamples.append(y[time[0]:time[1]])
    return transientSamples


def getTransientLocations(y: np.ndarray, midiFile: Optional[str] = None, sr: int = 44100) -> [(int, int)]:
    """Takes the path to an audio file
    and returns the list of start and stop times for that audio file
    as a frame rate. The midi file would have the correct start and stop times.

    :param fileName: The path to an audio file
    :param sr: The sample rate of the audio file. Defaults to 44100.

    :return: A list of start and stop times for each sound change
    """

    if midiFile:
        onsets = getOnsetsFromMidi(midiFile, sr)
    else:
        onsets = getOnsets(y, sr)
    transientLocations = onsetsToTransientLocations(onsets)
    return transientLocations


def saveTransients(y: np.ndarray, outputFolder: str, midiFile: Optional[str] = None, sr: int = 44100):
    if (os.path.exists(outputFolder)):
        shutil.rmtree(outputFolder)
    os.mkdir(outputFolder)

    transientLocations = getTransientLocations(y, midiFile=midiFile, sr=sr)
    transientSamples = locationsToSamples(y, transientLocations)

    for sample in range(len(transientSamples)):
        filename = os.path.join(outputFolder, 'sample_' + str(sample) + '.wav')
        sf.write(filename, transientSamples[sample], sr)


def locationsToSpectrograms(y: np.ndarray, locations):
    samples = locationsToSamples(y, locations)
    return [np.abs(librosa.stft(y)) for y in samples]


def main():

    # soundFile = os.path.join(assets, 'sound-files/first-four-seconds.wav')
    # midiFile = os.path.join(assets, 'midi/first-four-seconds.mid')
    # sr = librosa.get_samplerate(soundFile)
    return


main()
