import matplotlib.pyplot as plt
import numpy as np
from ez_load import ez_load
from parser import parser
from sorting import (
    sort_by_hardness,
    # sort_by_depth,
    # sort_by_brightness,
    sort_by_roughness,
    sort_by_warmth,
    sort_by_sharpness,
    sort_by_boominess,
    sort_by_reverb,
)
from split_transients import get_transient_locations


def diff_matrix(
    values,
    outfile,
    gridline=1,
):
    plt.figure()
    max_spec = 0

    for i in range(len(values)):
        (index, value) = values[i]
        value = value
        plt.text(
            i,
            value,
            index,
            fontsize=4
        )
        if value > max_spec:
            max_spec = value

    plt.xticks([])
    plt.xlim([0, len(values)])
    # plt.ylim()
    plt.yticks(
        np.arange(0, max_spec * 1.1, gridline),
        fontsize=4
    )
    plt.ylabel('Value')
    plt.grid()
    plt.savefig(outfile)


def main():
    args = parser.parse_args()  # infile, outfile, midi, sr
    y, sr = ez_load(args.infile, args.sr)

    if (args.midi):
        transient_locations = get_transient_locations(y, args.midi, sr=sr)
    else:
        transient_locations = get_transient_locations(y, sr=sr)

    diff_matrix(values=sort_by_hardness(y, sr, transient_locations), outfile='hardness.png')
    # diff_matrix(values=sortByDepth(y, sr, transient_locations), outfile='depth.png')
    # diff_matrix(values=sortByBrightness(y, sr, transient_locations), outfile='brightness.png')
    diff_matrix(values=sort_by_roughness(y, sr, transient_locations), outfile='roughness.png')
    diff_matrix(values=sort_by_warmth(y, sr, transient_locations), outfile='warmth.png')
    diff_matrix(values=sort_by_sharpness(y, sr, transient_locations), outfile='sharpness.png')
    diff_matrix(values=sort_by_boominess(y, sr, transient_locations), outfile='boominess.png')
    diff_matrix(values=sort_by_reverb(y, sr, transient_locations), outfile='reverb.png')


main()
