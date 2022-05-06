import pretty_midi
import librosa

from typing import List, Tuple


def createTrackFromTime(
    intervals: List[Tuple[int, int]],
    note: str = 'A3',
    instrument_name: str = 'Acoustic Grand Piano',
    velocity: int = 100
) -> pretty_midi.Instrument:
    """
    Takes a list of start and stop times that this sound plays and writes a track with those start and stop times
    :param intervals: A list of start and stop times
    :param note: Defaults to 'A3'.
    :param instrument: The instrument this midi track is recorded as. Defaults to 'Acoustic Grand Piano'.
    :param velocity: Defaults to 100.
    :return: An instrument that can be added to a midi
    """

    program = pretty_midi.instrument_name_to_program(instrument_name)
    instrument = pretty_midi.Instrument(program=program)
    noteNumber = pretty_midi.note_name_to_number(note)
    for times in intervals:
        start = times[0]
        stop = times[1]
        # Divide by 1000 to account for that other thing that doesn't make sense. Search for "sense"
        note = pretty_midi.Note(velocity=velocity, pitch=noteNumber, start=(start)/1000, end=(stop)/1000)
        instrument.notes.append(note)
    return instrument


def createMidiFromLocations(locations: List[Tuple[int, int]], outfile: str = "midi_file.mid"):
    """
    Takes a list of start and stop times for sounds, and creates a midi when each sound is a track
    :param locations: each tuple contains the start and stop times that this sound occurs
    :param outfile: the file to print to
    """

    midi = pretty_midi.PrettyMIDI()
    # soundList = alignTimesToStart(soundList)

    for sound in locations:
        track = createTrackFromTime(librosa.samples_to_time(sound))
        midi.instruments.append(track)

    midi.write(outfile)
