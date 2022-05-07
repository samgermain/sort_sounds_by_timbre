from typing import List, Tuple

import librosa
import pretty_midi
import numpy as np


def create_sample(
    start: float,
    stop: float,
    note: str = 'A3',
    instrument_name: str = 'Acoustic Grand Piano',
    velocity: int = 100
) -> pretty_midi.Instrument:
    """
    Takes a start and stop times that this sound plays and writes a track with that start and stop time
    :param start: Start time
    :param stop: Stop time
    :param note: Defaults to 'A3'
    :param instrument: The instrument this midi track is recorded as. Defaults to 'Acoustic Grand Piano'
    :param velocity: Defaults to 100
    :return: An instrument that can be added to a midi
    """

    program = pretty_midi.instrument_name_to_program(instrument_name)
    instrument = pretty_midi.Instrument(program=program)
    note_number = pretty_midi.note_name_to_number(note)
    # Divide by 1000 to account for that other thing that doesn't make sense. Search for "sense"
    note = pretty_midi.Note(velocity=velocity, pitch=note_number, start=(start)/1000, end=(stop)/1000)
    instrument.notes.append(note)
    return instrument


def create_midi_from_locations(
    locations: List[Tuple[int, int]],
    sr,
    outfile: str = "outfile.mid",
):
    """
    Takes a list of start and stop times for sounds, and creates a midi when each sound is a track
    :param locations: each tuple contains the start and stop times that this sound occurs
    :param outfile: the file to print to
    """

    midi = pretty_midi.PrettyMIDI()
    # sound_list = align_times_to_start(sound_list)

    for sound in locations:
        [start, stop] = librosa.samples_to_time(samples=sound, sr=sr)
        track = create_sample(start, stop)
        midi.instruments.append(track)

    midi.write(outfile)
