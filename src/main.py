import librosa
import argparse
from splitTransients import get_transient_locations
from sortSounds import sort_locations_by_coef, sort_locations_by_time_and_coef
from create_midi_files import create_midi_from_locations

def ez_load(sound_file, sr = None):
    if sr:
        y, sr = librosa.load(sound_file, sr=sr)
    else:
        y, sr = librosa.load(sound_file)
    return y, sr

parser = argparse.ArgumentParser(description='Create a plot of each sound in the sound, sorted by sound similarity. x=time')
parser.add_argument('-i', '--infile', type=str, default='../assets/sound-files/first-four-seconds.wav')    #The sound file to read from
parser.add_argument('-o', '--outfile', type=str, default='../assets/midi/midi_file.mid')   #The midi file to write to
parser.add_argument('-m', '--midi', type=str)   #If there is a midi file to base start and stop times off of
parser.add_argument('-s', '--sr', type=int, default=44100)
args = parser.parse_args()

y, sr = ez_load(args.infile, args.sr)

if (args.midi):
    transient_locations = get_transient_locations(y, args.midi)
else:
    transient_locations = get_transient_locations(y)

sorted_locations = sort_locations_by_time_and_coef(y, transient_locations)
create_midi_from_locations(sorted_locations, args.outfile)