import librosa
import argparse
from split_transients import transients_from_sound_file, transients_from_midi
from sort_sounds import sort_sounds
from create_midi_files import create_midi_from_sound_list

parser = argparse.ArgumentParser(description='Create a plot of each sound in the sound, sorted by sound similarity. x=time')
parser.add_argument('-i', '--input', type=str, default='../sound-files/first-four-seconds.wav')
# parser.add_argument('-o', '--output', type=str, default='transients')
parser.add_argument('-m', '--midi', type=str)
parser.add_argument('-s', '--sr', type=int, default=44100)
args = parser.parse_args()

if (args.midi):
    transients = transients_from_midi(args.midi, args.input)
else:
    transients = transients_from_sound_file(args.input)

sounds = sort_sounds(transients, args.input)
create_midi_from_sound_list(sounds)