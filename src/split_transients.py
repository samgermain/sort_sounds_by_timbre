# import matplotlib.pyplot as plt
import os
import shutil
from typing import List, Optional

import librosa
import numpy as np
import pretty_midi
import soundfile as sf

# from config import assets


def get_onsets_from_midi(midi_file: str, sr: int):
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    onsets = midi_data.get_onsets()
    arr = np.array(onsets)
    return librosa.core.time_to_samples(times=arr, sr=sr)


def get_onsets(y: np.ndarray, sr: int):
    C = np.abs(librosa.cqt(y=y, sr=sr))
    o_env = librosa.onset.onset_strength(sr=sr, S=librosa.amplitude_to_db(C, ref=np.max))
    onsets = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)
    return librosa.frames_to_samples(onsets)


def onsets_to_transient_locations(onset_samples: List[int]):
    """Takes a list of onset times for an audio file and returns the list of start and stop times for that audio file
    :param [int] onset_samples: I don't really know what these are actually.
        I thought they were start times for each sound change but I don't know
    :return [(int, int)]: A list of start and stop times for each sound change
    """

    starts = onset_samples[0:-1]
    stops = onset_samples[1:]
    transient_times = []
    for s in range(len(starts)):
        transient_times.append([starts[s], stops[s]])
    return np.array(transient_times)


def locations_to_samples(y: np.ndarray, transient_locations):
    transient_samples = []

    for time in transient_locations:
        transient_samples.append(y[time[0]:time[1]])
    return transient_samples


def get_transient_locations(y: np.ndarray, midi_file: Optional[str] = None, sr: int = 44100) -> [(int, int)]:
    """Takes the path to an audio file
    and returns the list of start and stop times for that audio file
    as a frame rate. The midi file would have the correct start and stop times.

    :param fileName: The path to an audio file
    :param sr: The sample rate of the audio file. Defaults to 44100.

    :return: A list of start and stop times for each sound change
    """

    if midi_file:
        onsets = get_onsets_from_midi(midi_file, sr)
    else:
        onsets = get_onsets(y, sr)
    transient_locations = onsets_to_transient_locations(onsets)
    return transient_locations


def save_transients(y: np.ndarray, output_folder: str, midi_file: Optional[str] = None, sr: int = 44100):
    if (os.path.exists(output_folder)):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    transient_locations = get_transient_locations(y, midi_file=midi_file, sr=sr)
    transient_samples = locations_to_samples(y, transient_locations)

    for sample in range(len(transient_samples)):
        filename = os.path.join(output_folder, 'sample_' + str(sample) + '.wav')
        sf.write(filename, transient_samples[sample], sr)


def locations_to_spectrograms(y: np.ndarray, locations):
    samples = locations_to_samples(y, locations)
    return [np.abs(librosa.stft(y)) for y in samples]


def main():

    # sound_file = os.path.join(assets, 'sound-files/first-four-seconds.wav')
    # midi_file = os.path.join(assets, 'midi/first-four-seconds.mid')
    # sr = librosa.get_samplerate(sound_file)
    return


main()