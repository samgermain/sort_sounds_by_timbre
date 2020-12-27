import numpy as np
import librosa

def getSpecList(samples):
    S = [np.abs(librosa.stft(y)) for y in samples]
    S = [np.array(s) for s in S]
    return S

def getSimilarityCoefficients(S):
    similarity_coefficents = []
    length = min([s.shape[1] for s in S])   #TODO: improve this, it's probably not the best
    for index1 in range(len(S)):
        diffs = []
        for index2 in range(len(S)):
            diff = S[index1][:,:length] - S[index2][:,:length]
            diffs.append(diff)
        sc = [np.sum(diff) for diff in diffs]
        # similarity_coefficents.append(np.abs(sc))
        similarity_coefficents.append(sc)
    return(similarity_coefficents)

def sortSoundsByCoef(times, samples):
    """
    Sorts all the sounds in a sound file by sound similarity. Longer sounds are cropped to the length of the shortest sounds
    Args:
        times ([(int, int)]): A list of the start and stop times of each sound in a soundFile
        samples (string): The clips of the sound file
    Return:
        ([[(int, int)]]): A list of lists where each sublist contains the start and stop times the sound it represents is playing
    """
    
    S = getSpecList(samples)
    sc = getSimilarityCoefficients(S)
    times = [[t] for _,t in sorted(zip(sc[0], times))]
    
    return times

def sortSoundsByTimeAndCoef(times, samples):
    """Sounds are only compared to eachother if they are the same length in time

    Args:
        times ([type]): List of start and stop times for sounds
        samples ([type]): The sounds that correspond to those start and stop times
    """
    # for s in samples:
    #     print(s.shape)
    S = getSpecList(samples)    #STFT spectrograms
    # for s in S:
    #     print(s.shape)
    lengths = set([s.shape[1] for s in S])    #Duration of sounds
    sortedTimes = []
    for l in lengths:
        subList = [(S[i], times[i]) for i in range(len(S)) if S[i].shape[1] == l]   #Spectrograms and start/stop times for sounds of the same length
        subS = [s for s,_ in subList]       #Spectrograms for sounds of the same length
        subTimes = [t for _,t in subList ]  #Start/stop times for sounds of the same length
        sc = getSimilarityCoefficients(subS)
        newSortedTimes = [[t] for _,t in sorted(zip(sc,subTimes))]  #In the end version, there may be multiple sounds on the same line
        sortedTimes += newSortedTimes
    return np.array(sortedTimes)