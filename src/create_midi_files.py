import pretty_midi
from librosa import frames_to_time

def create_track_from_time(intervals, note='A3', instrument='Acoustic Grand Piano', velocity=100):
    """Takes a list of start and stop times that this sound plays and writes a track with those start and stop times

    Args:
        intervals ([(int, int)]): A list of start and stop times
        note (str, optional): Defaults to 'A3'.
        instrument (str, optional): The instrument this midi track is recorded as. Defaults to 'Acoustic Grand Piano'.
        velocity (int, optional): Defaults to 100.

    Returns:
        (Instrument): An instrument that can be added to a midi
    """

    program = pretty_midi.instrument_name_to_program(instrument)
    instrument = pretty_midi.Instrument(program=program)
    note_number = pretty_midi.note_name_to_number(note)
    for times in intervals:
        start = times[0]
        stop = times[1]
        note = pretty_midi.Note(velocity=velocity, pitch=note_number, start=(start)/1000, end=(stop)/1000)  #Divide by 1000 to account for that other thing that doesn't make sense. Search for "sense"
        instrument.notes.append(note)
    return instrument

# def alignTimesToStart(soundList):
#     """When there's a gap at the beginning, then moves all the sounds to the left, so that there's no gap at the beginning

#     Args:
#         soundList ([(int, int)]): start and stop time

#     Returns:
#         ([(int, int)]): start and stop time
#     """
#     print(soundList)
#     first = min([times[0] for times in soundList]) #need to subtract first because the time is off, don't know if this is where I should subtract it
#     return [[times[0] - first, times[1] - first] for times in soundList ]

def create_midi_from_sound_list(soundList, outfile="midi_file.mid"):
    """
    Takes a list of start and stop times for sounds, and creates a midi when each sound is a track

    Args:
        soundList ([[(int, int)]]): each tuple contains the start and stop times that this sound occurs
    """
    
    midi = pretty_midi.PrettyMIDI()
    # soundList = alignTimesToStart(soundList)

    for sound in soundList:
        track = create_track_from_time(frames_to_time(sound))
        midi.instruments.append(track)

    midi.write(outfile)
