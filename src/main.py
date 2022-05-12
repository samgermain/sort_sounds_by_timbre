from create_midi_files import create_multi_midi_from_locations
from sorting import (
    sort_by_hardness,
    # sort_by_depth,
    # sort_by_brightness,
    sort_by_roughness,
    sort_by_warmth,
    sort_by_sharpness,
    sort_by_boominess,
    sort_by_reverb,
    sort_by_spectra_of_spectra,
)
from split_transients import get_transient_locations
from ez_load import ez_load
from parser import parser


args = parser.parse_args()  # infile, outfile, midi, sr
y, sr = ez_load(args.infile, args.sr)

if (args.midi):
    transient_locations = get_transient_locations(y, args.midi, sr=sr)
else:
    transient_locations = get_transient_locations(y, sr=sr)

create_multi_midi_from_locations(
    [
        sort_by_hardness(y, sr, transient_locations),
        # sort_by_depth(y, sr, transient_locations),
        # sort_by_brightness(y, sr, transient_locations),
        sort_by_roughness(y, sr, transient_locations),
        sort_by_warmth(y, sr, transient_locations),
        sort_by_sharpness(y, sr, transient_locations),
        sort_by_boominess(y, sr, transient_locations),
        sort_by_reverb(y, sr, transient_locations),
        sort_by_spectra_of_spectra(y, transient_locations)
    ],
    sr,
    args.outfile,
)
