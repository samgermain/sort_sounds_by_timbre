import numpy as np
import librosa
from splitTransients import locationsToSpectrograms, locationsToSamples
import matplotlib.pyplot as plt

def getSimilarityCoefficients(S):
    """Takes a list of spectrograms and returns a list of lists where each sublist contains the similarity coefficents between the corresponding list in S and every other spectrogram in S

    Args:
        S ([[float][float]]): A list of spectrograms
    Return:
        [[float]]: Similarity coefficents between each spectrogram, to every other spectrogram per sublist
    """
    similarity_coefficents = []
    # flat = np.ndarray.flatten(similarity_coefficents)
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

def sortLocationsByCoef(y, locations):
    """
    Sorts all the sounds in a sound file by sound similarity. Longer sounds are cropped to the length of the shortest sounds
    Args:
        times ([(int, int)]): A list of the start and stop times of each sound in a soundFile
        samples (string): The clips of the sound file
    Return:
        ([[(int, int)]]): A list of lists where each sublist contains the start and stop times the sound it represents is playing
    """
    S = locationsToSpectrograms(y, locations)
    sc = getSimilarityCoefficients(S)
    return [[l] for _,l in sorted(zip(sc[0], locations))]

def sortLocationsByTimeAndCoef(y, locations):
    
    """Sounds are only compared to eachother if they are the same length in time

    Args:
        times ([type]): List of start and stop times for sounds
        samples ([type]): The sounds that correspond to those start and stop times
    """

    S = locationsToSpectrograms(y, locations)
    lengths = set([s.shape[1] for s in S])    #Duration of sounds
    
    sortedLocations = []
    for l in lengths:

        subList = [(S[i], locations[i]) for i in range(len(S)) if S[i].shape[1] == l]   #Spectrograms and start/stop times for sounds of the same length
        subSpec = [s for s,_ in subList]       #Spectrograms for sounds of the same length
        subLocations = [l for _,l in subList ]  #Start/stop times for sounds of the same length
        
        sc = getSimilarityCoefficients(subSpec)
        newSortedLocations = [[s] for _,s in sorted(zip(sc,subLocations))]  #In the end version, there may be multiple sounds on the same line
        sortedLocations += newSortedLocations
    
    return np.array(sortedLocations)

def convertSamplesToMfcc(y, sr, locations):
    samples = locationsToSamples(y, locations)
    # mfcc = librosa.feature.mfcc(samples[0], n_mfcc=13, sr=sr)
    # delta_mfcc = librosa.feature.delta(mfcc)
    # delta2_mfcc = librosa.feature.delta(mfcc, order=2)
    # return mfcc, delta_mfcc, delta2_mfcc
    mfccs = [librosa.feature.mfcc(s, n_mfcc=13, sr=sr) for s in samples]
    delta_mfccs = [librosa.feature.delta(m, mode="nearest") for m in mfccs]
    delta2_mfccs = [librosa.feature.delta(m, mode="nearest", order=2) for m in mfccs]
    return mfccs, delta_mfccs, delta2_mfccs
