import argparse


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
