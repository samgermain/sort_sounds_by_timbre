from create_midi_files import create_midi_from_locations
from sort_sounds import sort_locations_by_spectra_of_spectra
from split_transients import get_transient_locations
from ez_load import ez_load
from parser import parser


args = parser.parse_args()
y, sr = ez_load(args.infile, args.sr)

if (args.midi):
    transient_locations = get_transient_locations(y, args.midi, sr=sr)
else:
    transient_locations = get_transient_locations(y, sr=sr)

sorted_locations = sort_locations_by_spectra_of_spectra(y, transient_locations)
create_midi_from_locations(sorted_locations, sr, args.outfile)
