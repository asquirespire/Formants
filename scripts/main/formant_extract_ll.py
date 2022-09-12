# modules
import pandas as pd
import os
from os.path import join
import numpy as np
from tqdm import tqdm

from scipy.io.wavfile import write
import librosa
import parselmouth
from parselmouth.praat import call
import praat_formants_python.praat_formants_python as pfp

from multiprocessing import Process

ALL_EXP_FOLDER = (
    "/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/CSV2/tmp_min_ll"
)
if not os.path.exists(ALL_EXP_FOLDER):
    os.mkdir(ALL_EXP_FOLDER)

ALL_TIMIT_VOWELS_EXP_FILEPATH = "/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/CSV2/timit-vowels_subset_2.csv"
ALL_TIMIT_VOWELS_DF_FPE = pd.read_csv(ALL_TIMIT_VOWELS_EXP_FILEPATH)


def measureFormants(audio_path, start_sec, end_sec, vowel_type):
    f0min, f0max = [75, 500]
    sound = parselmouth.Sound(audio_path)  # read the sound
    pitch = call(
        sound, "To Pitch (cc)", 0, f0min, 15, "no", 0.03, 0.45, 0.01, 0.35, 0.14, f0max
    )
    mean_pitch = call(pitch, "Get mean", 0, 0, "Hertz")  # get mean pitch

    audio_chunk, fs = librosa.load(
        audio_path, sr=None, offset=start_sec, duration=(end_sec - start_sec)
    )
    tmp_audio_file = f"/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/AUDIO/tmp_timit_phones/{vowel_type}.wav"
    write(tmp_audio_file, fs, audio_chunk)

    sound_frm = parselmouth.Sound(tmp_audio_file)
    # sound_frm = sound_frm.extract_part(rom_time=start_sec, to_time=end_sec, window_shape=0, relative_width=1, preserve_times=False) # read the sound chunk
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    formants = call(sound_frm, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    numPoints = call(pointProcess, "Get number of points")

    f1_list = []
    f2_list = []
    f3_list = []
    f4_list = []

    # Measure formants only at glottal pulses
    for point in range(0, numPoints):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, "Hertz", "Linear")
        f2 = call(formants, "Get value at time", 2, t, "Hertz", "Linear")
        f3 = call(formants, "Get value at time", 3, t, "Hertz", "Linear")
        f4 = call(formants, "Get value at time", 4, t, "Hertz", "Linear")
        f1_list.append(f1)
        f2_list.append(f2)
        f3_list.append(f3)
        f4_list.append(f4)

    f1_list = [f1 for f1 in f1_list if str(f1) != "nan"]
    f2_list = [f2 for f2 in f2_list if str(f2) != "nan"]
    f3_list = [f3 for f3 in f3_list if str(f3) != "nan"]
    f4_list = [f4 for f4 in f4_list if str(f4) != "nan"]

    # calculate mean formants across pulses
    f1_mean = np.mean(f1_list)
    f2_mean = np.mean(f2_list)
    f3_mean = np.mean(f3_list)
    f4_mean = np.mean(f4_list)

    # calculate median formants across pulses, this is what is used in all subsequent calcualtions
    # you can use mean if you want, just edit the code in the boxes below to replace median with mean
    f1_median = np.median(f1_list)
    f2_median = np.median(f2_list)
    f3_median = np.median(f3_list)
    f4_median = np.median(f4_list)

    return (
        mean_pitch,
        f1_mean,
        f2_mean,
        f3_mean,
        f4_mean,
        f1_median,
        f2_median,
        f3_median,
        f4_median,
    )


def measure_pitch(audio_path):
    f0min, f0max = [75, 500]

    sound = parselmouth.Sound(audio_path)  # read the sound
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max)  # create a praat pitch object
    mean_pitch = call(pitch, "Get mean", 0, 0, "Hertz")  # get mean pitch
    return mean_pitch


def measureFormants2(audio_path, start_sec, end_sec):
    formants = pfp.formants_at_interval(
        audio_path, start_sec, end_sec, maxformant=5500, winlen=0.025, preemph=50
    )

    formants_mean = formants.mean(axis=0)
    formants_mean = list(formants_mean)[1:]  # skip time

    formants_median = np.median(formants, axis=0)
    formants_median = list(formants_median)[1:]  # skip time

    pitch_mean = measure_pitch(audio_path)

    return (
        pitch_mean,
        formants_mean[0],
        formants_mean[1],
        formants_mean[2],
        formants_median[0],
        formants_median[1],
        formants_median[2],
    )


dfs_list = np.array_split(ALL_TIMIT_VOWELS_DF_FPE, 8)


def vowel_formant_estimation(df: pd.DataFrame):

    split_id = df.iloc[0, :]["idx"]
    ALL_TIMIT_VOWELS_FPE_EXP_FILENAME = (
        f"all_timit_vowels_formant_estimation_ll-{split_id}.csv"
    )

    ALL_TIMIT_VOWELS_FPE_ARR: list[dict] = []
    for _, _vowel in tqdm(df.iterrows()):

        # Praat: pitch and formant estimation
        (
            pitch,
            f1_mean,
            f2_mean,
            f3_mean,
            f1_median,
            f2_median,
            f3_median,
        ) = measureFormants2(
            _vowel["audio_filepath"],
            _vowel["start_second"],
            _vowel["end_second"],
        )

        _row = [
            {
                "idx": _vowel["idx"],
                "person": _vowel["person"],
                "vowel_type": _vowel["vowel_type"],
                "pitch_org_praat": pitch,
                "f1_mean_org_praat": f1_mean,
                "f2_mean_org_praat": f2_mean,
                "f3_mean_org_praat": f3_mean,
                "f1_median_org_praat": f1_median,
                "f2_median_org_praat": f2_median,
                "f3_median_org_praat": f3_median,
            }
        ]

        ALL_TIMIT_VOWELS_FPE_ARR += _row

        # break

    ALL_TIMIT_VOWELS_FPE_EXP_FILEPATH = join(
        ALL_EXP_FOLDER, ALL_TIMIT_VOWELS_FPE_EXP_FILENAME
    )

    ALL_TIMIT_VOWELS_FPE_DF = pd.DataFrame(ALL_TIMIT_VOWELS_FPE_ARR)

    ALL_TIMIT_VOWELS_FPE_DF.to_csv(ALL_TIMIT_VOWELS_FPE_EXP_FILEPATH, index=False)


if __name__ == "__main__":
    for d in dfs_list:
        p = Process(target=vowel_formant_estimation, args=(d,))
        p.start()
        # p.join()
