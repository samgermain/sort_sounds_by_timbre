import librosa
import argparse
from split_transients import transients_from_sound_file, transients_from_midi
from sort_sounds import sort_sounds
from create_midi_files import create_midi_from_sound_list

parser = argparse.ArgumentParser(description='Create a plot of each sound in the sound, sorted by sound similarity. x=time')
parser.add_argument('-i', '--infile', type=str, default='../sound-files/first-four-seconds.wav')    #The sound file to read from
parser.add_argument('-o', '--outfile', type=str, default='midi_file.mid')   #The midi file to write to
parser.add_argument('-m', '--midi', type=str)   #If there is a midi file to base start and stop times off of
parser.add_argument('-s', '--sr', type=int, default=44100)
args = parser.parse_args()

if (args.midi):
    transientTimes, transientSamples = transients_from_midi(args.midi, args.infile)
else:
    transientTimes, transientSamples = transients_from_sound_file(args.infile)

rms = []
for sample in transientSamples:
    rms.append(librosa.feature.rms(y=sample)[0])
    
print(rms)

sortedSounds = sort_sounds(transientTimes, transientSamples)
create_midi_from_sound_list(sortedSounds, args.outfile)