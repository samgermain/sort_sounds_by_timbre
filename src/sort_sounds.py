# import matplotlib.pyplot as plt
from typing import List, Tuple

import numpy as np

from split_transients import locations_to_samples, locations_to_spectrograms


def spectra_of_spectra(sample: np.ndarray):
    '''
    Step 2: Calculate the PSD of the PSD and integrate (or really just sum):
    Dividing by the length (normalizing) helps to compare different files of different lengths.
    '''
    # first calculate the psd
    fft = np.fft.fft(sample)
    fft = fft[:len(fft)//2+1]
    psd1 = np.real(fft * np.conj(fft))
    # then calculate the psd of the psd
    fft = np.fft.fft(psd1/sum(psd1))
    fft = fft[:len(fft)//2+1]
    psd = np.real(fft * np.conj(fft))
    return(np.sum(psd)/len(psd))


def get_similarity_coefficients(S: List[np.ndarray]) -> List[List[float]]:
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


def sort_locations_by_coef(
    y: np.ndarray,
    locations: List[Tuple[int, int]]
) -> List[List[Tuple[int, int]]]:
    """
    # ! Bad
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


def sort_locations_by_time_and_coef(
    y: np.ndarray,
    locations: List[Tuple[int, int]]
):
    """
    # ! Bad
    Sounds are only compared to eachother if they are the same length in time

    :param y:
    :param locations: List of start and stop times for sounds
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
        sub_spec = [s for s, _ in sub_list]
        # Start/stop times for sounds of the same length
        sub_locations = [l for _, l in sub_list]

        sc = get_similarity_coefficients(sub_spec)
        # In the end version, there may be multiple sounds on the same line
        new_sorted_locations = [[s] for _, s in sorted(zip(sc, sub_locations))]
        sorted_locations += new_sorted_locations

    return np.array(sorted_locations)


def sort_locations_by_spectra_of_spectra(
    y: np.ndarray,
    locations: List[Tuple[int, int]]
):
    """
    :param y: sound file processed by librosa
    :param locations: List of start and stop times for sounds
    """

    samples = locations_to_samples(y, locations)
    values = [spectra_of_spectra(sample) for sample in samples]
    sorted_values = sorted(enumerate(values), key=lambda x: x[1], reverse=True)
    sorted_order = [i[0] for i in sorted_values]
    sorted_locations = [locations[i] for i in sorted_order]

    grouped_values = [[sorted_values[0]]]
    grouped_locations = [[sorted_locations[0]]]
    for i in range(1, len(sorted_values)):
        [_, value] = sorted_values[i]
        [_, past_value] = grouped_values[-1][-1]
        if abs(value - past_value) < 0.01:
            grouped_values[-1].append(value)
            grouped_locations[-1].append(sorted_locations[i])

    return(grouped_locations)
