
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
    starts = onset_samples[0:-1]
    stops = onset_samples[1:]
    transients = []
    for s in range(len(starts)):
        transients.append((starts[s], stops[s]))
    return transients

def transients_from_sound_file(fileName, sr=44100):
    y, sr = ezLoad(fileName, sr)
    C = np.abs(librosa.cqt(y=y, sr=sr))
    o_env = librosa.onset.onset_strength(sr=sr, S=librosa.amplitude_to_db(C, ref=np.max))
    onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)

    onset_samples = list(librosa.frames_to_samples(onset_frames))
    onset_samples = np.concatenate(onset_samples, len(y))
    return transients_from_onsets(onset_samples)

def transients_from_midi(midiFile, soundFile, sr=41000):
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

main()