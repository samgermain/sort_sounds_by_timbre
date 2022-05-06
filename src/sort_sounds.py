# import matplotlib.pyplot as plt
from typing import List, Tuple

import librosa
import numpy as np
from splitTransients import locations_to_samples, locations_to_spectrograms


def get_similarity_coefficients(S: List[Tuple[List[float], List[float]]]) -> List[List[float]]:
    """
    Takes a list of spectrograms and returns a list of lists where each sublist contains the similarity coefficents
        between the corresponding list in S and every other spectrogram in S
    :param S: A list of spectrograms
    :return: Similarity coefficents between each spectrogram, to every other spectrogram per sublist
    """
    similarity_coefficents = []
    # flat = np.ndarray.flatten(similarity_coefficents)
    # TODO: improve this, it's probably not the best
    length = min([s.shape[1] for s in S])
    for index1 in range(len(S)):
        diffs = []
        for index2 in range(len(S)):
            diff = S[index1][:, :length] - S[index2][:, :length]
            diffs.append(diff)
        sc = [np.sum(diff) for diff in diffs]
        # similarity_coefficents.append(np.abs(sc))
        similarity_coefficents.append(sc)
    return(similarity_coefficents)


def sort_locations_by_coef(y: np.ndarray, locations: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    """
    Sorts all the sounds in a sound file by sound similarity. Longer sounds are cropped to the length of the 
        shortest sounds
    :param samples: The clips of the sound file
    :param times: A list of the start and stop times of each sound in a sound_file
    :return: A list of lists where each sublist contains the start and stop times the sound
        it represents is playing
    """
    S = locations_to_spectrograms(y, locations)
    sc = get_similarity_coefficients(S)
    return [[l] for _, l in sorted(zip(sc[0], locations))]


def sort_locations_by_time_and_coef(y, locations):
    """Sounds are only compared to eachother if they are the same length in time

    Args:
        times ([type]): List of start and stop times for sounds
        samples ([type]): The sounds that correspond to those start and stop times
    """

    S = locations_to_spectrograms(y, locations)
    lengths = set([s.shape[1] for s in S])  # Duration of sounds

    sorted_locations = []
    for length in lengths:

        # Spectrograms and start/stop times for sounds of the same length
        sub_list = [
            (S[i], locations[i])
            for i in range(len(S))
            if S[i].shape[1] == length
        ]
        # Spectrograms for sounds of the same length
        subSpec = [s for s, _ in sub_list]
        # Start/stop times for sounds of the same length
        sub_locations = [l for _, l in sub_list]

        sc = get_similarity_coefficients(subSpec)
        # In the end version, there may be multiple sounds on the same line
        newSortedLocations = [[s] for _, s in sorted(zip(sc, sub_locations))]
        sorted_locations += newSortedLocations

    return np.array(sorted_locations)


def convert_samples_to_mfcc(y, sr, locations):
    samples = locations_to_samples(y, locations)
    # mfcc = librosa.feature.mfcc(samples[0], n_mfcc=13, sr=sr)
    # delta_mfcc = librosa.feature.delta(mfcc)
    # delta2_mfcc = librosa.feature.delta(mfcc, order=2)
    # return mfcc, delta_mfcc, delta2_mfcc
    mfccs = [librosa.feature.mfcc(s, n_mfcc=13, sr=sr) for s in samples]
    delta_mfccs = [librosa.feature.delta(m, mode="nearest") for m in mfccs]
    delta2_mfccs = [librosa.feature.delta(
        m, mode="nearest", order=2) for m in mfccs]
    return mfccs, delta_mfccs, delta2_mfccs
