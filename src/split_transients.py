
import matplotlib.pyplot as plt
import librosa
import numpy as np
import os
import soundfile as sf
import pretty_midi

def ezLoad(soundFile, sr = None):
    if sr:
        y, sr = librosa.load(soundFile, sr=sr)
    else:
        y, sr = librosa.load(soundFile)
    return y, sr

def transients_from_onsets(onset_samples):
    """Takes a list of onset times for an audio file and returns the list of start and stop times for that audio file

    Args:
        onset_samples ([int]): I don't really know what these are actually. I thought they were start times for each sound change but I don't know

    Returns:
        [(int, int)]: A list of start and stop times for each sound change
    """
    starts = onset_samples[0:-1]
    stops = onset_samples[1:]
    transients = []
    for s in range(len(starts)):
        transients.append((starts[s], stops[s]))
    return transients

def transients_from_sound_file(fileName, sr=44100):
    """Takes the path to an audio file
    and returns the list of start and stop times for that audio file
    as a frame rate

    Args:
        fileName (string): The path to an audio file
        sr (int, optional): The sample rate of the audio file. Defaults to 44100.

    Returns:
        [(int, int)]: A list of start and stop times for each sound change
    """
    y, sr = ezLoad(fileName, sr)
    C = np.abs(librosa.cqt(y=y, sr=sr))
    o_env = librosa.onset.onset_strength(sr=sr, S=librosa.amplitude_to_db(C, ref=np.max))
    onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)

    onset_samples = list(librosa.frames_to_samples(onset_frames))
    onset_samples = np.concatenate(onset_samples, len(y))
    transients =  transients_from_onsets(onset_samples)
    return transients

def transients_from_midi(midiFile, soundFile, sr=44100):
    """Takes the path to an audio file, as well as the path to a midi file
     and returns the list of start and stop times for that audio file
    as a frame rate. The midi file would have the correct start and stop times. 
    The soundFile arg is useless if you provide the sample rate, it's there in case
    I end up deciding that I want to detemine the sample rate. The sample rate is
    only useful for converting time to frames

    Args:
        midiFile (string): The path to a midi file
        fileName (string): The path to an audio file
        sr (int, optional): The sample rate of the audio file. Defaults to 44100.


    Returns:
        [(int, int)]: A list of start and stop times for each sound change
    """

    y, sr = ezLoad(soundFile, sr)
    midi_data = pretty_midi.PrettyMIDI(midiFile)
    onsets = midi_data.get_onsets()
    arr = np.array(onsets)
    samples = librosa.core.time_to_samples(times=arr, sr=sr)
    transients = transients_from_onsets(samples)
    return transients    

def main():
    soundFile = "../sound-files/first-four-seconds.wav"
    midiFile = "../midi/first-four-seconds.mid"
    transients = transients_from_sound_file(soundFile)
    midiTransients = transients_from_midi(midiFile, soundFile)
    print(transients)
    print(midiTransients)

