from typing import List, Tuple, NewType

import librosa
import pretty_midi
# import numpy as np

Location = NewType('Location', Tuple[int, int])
LocationList = NewType('LocationList', List[Location])


def create_instrument(instrument_name: str = 'Acoustic Grand Piano'):
    """Creates a pretty_midi instrument from the instrument name"""
    program = pretty_midi.instrument_name_to_program(instrument_name)
    return pretty_midi.Instrument(program=program)


def add_note_to_instrument(
    instrument: pretty_midi.instrument,
    start: int,
    stop: int,
    sr: int,
    note: str = 'A3',
    velocity: int = 100,
):
    note_number = pretty_midi.note_name_to_number(note)
    note = pretty_midi.Note(
        velocity=velocity,
        pitch=note_number,
        start=start,
        end=stop,
    )
    instrument.notes.append(note)


def create_sample(
    locations: LocationList,
    sr: int,
    note: str = 'A3',
    instrument_name: str = 'Acoustic Grand Piano',
    velocity: int = 100
) -> pretty_midi.Instrument:
    """
    Takes a list of start and stop times that this sound plays and writes a track with those start and stop time
    :param note: Defaults to 'A3'
    :param instrument: The instrument this midi track is recorded as. Defaults to 'Acoustic Grand Piano'
    :param velocity: Defaults to 100
    :return: An instrument that can be added to a midi
    """

    instrument = create_instrument(instrument_name)
    for location in locations:
        [start, stop] = librosa.samples_to_time(samples=location, sr=sr)
        add_note_to_instrument(
            instrument=instrument,
            start=start,
            stop=stop,
            sr=sr,
            note=note,
            velocity=velocity,
        )
    return instrument


def create_multi_sample(
    locationLists: List[LocationList],
    sr: int,
    spacing: int = 4,
    note: str = 'A3',
    instrument_name: str = 'Acoustic Grand Piano',
    velocity: int = 100,
) -> pretty_midi.Instrument:
    """
    Takes a list of start and stop times that this sound plays and writes a track with those start and stop time
    :param locationsLists: A list of location lists, each item in the top list is spaced apart on the midi according 
        to the spaces in spacing
    :param note: Defaults to 'A3'
    :param instrument: The instrument this midi track is recorded as. Defaults to 'Acoustic Grand Piano'
    :param velocity: Defaults to 100
    :return: An instrument that can be added to a midi
    """

    instrument = create_instrument(instrument_name)
    for index in range(len(locationLists)):
        l: LocationList = locationLists[index]
        for location in l:
            [start, stop] = librosa.samples_to_time(samples=location, sr=sr)
            add_note_to_instrument(
                instrument=instrument,
                start=start + (index * spacing),
                stop=stop + (index * spacing),
                sr=sr,
                note=note,
                velocity=velocity,
            )
    return instrument


def create_midi_from_locations(
    locations: List[LocationList],
    sr: int,
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
        track = create_sample(
            locations=sound,
            sr=sr,
        )
        midi.instruments.append(track)

    midi.write(outfile)


def create_multi_midi_from_locations(
    locations: List[List[LocationList]],
    sr: int,
    outfile: str = "outfile.mid",
    spacing: int = '4',
):
    midi = pretty_midi.PrettyMIDI()

    listLengths = [len(list) for list in locations]

    for index in range(max(listLengths)):
        track = create_multi_sample(
            locationLists=[list[index] for list in locations if len(list) > index],
            sr=sr,
        )
        midi.instruments.append(track)

    midi.write(outfile)
