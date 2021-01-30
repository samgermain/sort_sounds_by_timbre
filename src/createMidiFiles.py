import pretty_midi
import librosa

def createTrackFromTime(intervals, note='A3', instrument='Acoustic Grand Piano', velocity=100):
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
    noteNumber = pretty_midi.note_name_to_number(note)
    for times in intervals:
        start = times[0]
        stop = times[1]
        note = pretty_midi.Note(velocity=velocity, pitch=noteNumber, start=(start)/1000, end=(stop)/1000)  #Divide by 1000 to account for that other thing that doesn't make sense. Search for "sense"
        instrument.notes.append(note)
    return instrument

def createMidiFromLocations(locations, outfile="midi_file.mid"):
    """
    Takes a list of start and stop times for sounds, and creates a midi when each sound is a track

    Args:
        soundList ([[(int, int)]]): each tuple contains the start and stop times that this sound occurs
    """
    
    midi = pretty_midi.PrettyMIDI()
    # soundList = alignTimesToStart(soundList)

    for sound in locations:
        track = createTrackFromTime(librosa.samples_to_time(sound))
        midi.instruments.append(track)

    midi.write(outfile)
