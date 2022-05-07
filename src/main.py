import argparse
from typing import Optional

import librosa

from create_midi_files import create_midi_from_locations
from sort_sounds import sort_locations_by_spectra_of_spectra
from split_transients import get_transient_locations


def ez_load(sound_file: str, sr: Optional[int] = None):
    if sr:
        y, sr = librosa.load(sound_file, sr=sr)
    else:
        y, sr = librosa.load(sound_file)
    return y, sr


parser = argparse.ArgumentParser(
    description='Create a plot of each sound in the sound, sorted by sound similarity'
)
required = parser.add_argument_group('required arguments')
required.add_argument(
    '-i',
    '--infile',
    type=str,
    required=True,
)
parser.add_argument(
    '-o',
    '--outfile',
    type=str,
    default='outfile.mid',  # The midi file to write to
)
# If there is a midi file to base start and stop times off of
parser.add_argument(
    '-m',
    '--midi',
    type=str,
    default=None,
    help='Output from Ableton right click -> slice to new midi track',
)
parser.add_argument('-s', '--sr', type=int, default=44100, help='sample rate')
args = parser.parse_args()

y, sr = ez_load(args.infile, args.sr)

if (args.midi):
    transient_locations = get_transient_locations(y, args.midi, sr=sr)
else:
    transient_locations = get_transient_locations(y, sr=sr)

sorted_locations = sort_locations_by_spectra_of_spectra(y, transient_locations)
create_midi_from_locations(sorted_locations, sr, args.outfile)
