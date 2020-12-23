def sort_sounds(transientTimes, transientSamples):
    """
    Sorts all the sounds in a sound file by sound similarity
    Args:
        transientTimes ([(int, int)]): A list of the start and stop times of each sound in a soundFile
        soundFile (string): The path to a sound file
    Return:
        ([[(int, int)]]): A list of lists where each sublist contains the start and stop times the sound it represents is playing
    """

    rms = []
    for sample in transientSamples:
        rms.append(librosa.feature.rms(y=sample)[0])
    #TODO: Finish rms values and sort    


    sounds = []
    for trs in transientTimes:
        sounds.append([trs])
    return sounds