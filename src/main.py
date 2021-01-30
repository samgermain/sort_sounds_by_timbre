import librosa
import argparse
from splitTransients import getTransientLocations
from sortSounds import sortLocationsByCoef, sortLocationsByTimeAndCoef
from createMidiFiles import createMidiFromLocations

def ezLoad(soundFile, sr = None):
    if sr:
        y, sr = librosa.load(soundFile, sr=sr)
    else:
        y, sr = librosa.load(soundFile)
    return y, sr

parser = argparse.ArgumentParser(description='Create a plot of each sound in the sound, sorted by sound similarity. x=time')
parser.add_argument('-i', '--infile', type=str, default='../assets/sound-files/first-four-seconds.wav')    #The sound file to read from
parser.add_argument('-o', '--outfile', type=str, default='../assets/midi/midi_file.mid')   #The midi file to write to
parser.add_argument('-m', '--midi', type=str)   #If there is a midi file to base start and stop times off of
parser.add_argument('-s', '--sr', type=int, default=44100)
args = parser.parse_args()

y, sr = ezLoad(args.infile, args.sr)

if (args.midi):
    transientLocations = getTransientLocations(y, args.midi)
else:
    transientLocations = getTransientLocations(y)

sortedLocations = sortLocationsByTimeAndCoef(y, transientLocations)
createMidiFromLocations(sortedLocations, args.outfile)