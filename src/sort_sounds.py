def sort_sounds(transients, soundFile):
    """
    Sorts all the sounds in a sound file by sound similarity
    Args:
        transients ([(int, int)]): A list of the start and stop times of each sound in a soundFile
        soundFile (string): The path to a sound file
    Return:
        ([[(int, int)]]): A list of lists where each sublist contains the start and stop times the sound it represents is playing
    """

    sounds = []
    for trs in transients:
        sounds.append([trs])
    return sounds