import pretty_midi

def create_track_from_time(intervals, note='A3', instrument='Acoustic Grand Piano', velocity=100):
    program = pretty_midi.instrument_name_to_program(instrument)
    instrument = pretty_midi.Instrument(program=program)
    note_number = pretty_midi.note_name_to_number(note)
    for (start, stop) in intervals:
        note = pretty_midi.Note(velocity=velocity, pitch=note_number, start=start, end=stop)
        instrument.notes.append(note)
    return instrument

def create_midi_from_sound_list(soundList, outfile="midi_file.mid"):
    """
    Takes a list of start and stop times for sounds, and creates a midi when each sound is a track

    Args:
        soundList ([[(int, int)]]): each tuple contains the start and stop times that this sound occurs
    """
    
    midi = pretty_midi.PrettyMIDI()

    for sound in soundList:
        track = create_track_from_time(sound)
        midi.instruments.append(track)

    midi.write(outfile)
