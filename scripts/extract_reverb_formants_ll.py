#!/home/jeevan/dev/anaconda3/envs/pytorch/bin/python


import pandas as pd
import numpy as np
from tqdm import tqdm
import os
import shutil
from os.path import join
import praat_formants_python.praat_formants_python as pfp
from scipy.fft import fft, ifft

from multiprocessing import Process

import librosa
import soundfile as sf

ALL_SYNTH_VOWEL_PATH = "/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/AUDIO/synth_vows_sample_set"
RIR_SIGNAL_PATH = (
    "/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/AUDIO/rir_impulse"
)

ALL_ORG_SYN_FORMANTS = "/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/exports/all_vowels_formants_org_synth.csv"

pfp.clear_formant_cache()

all_vowels_formants_org_synth_df = pd.read_csv(ALL_ORG_SYN_FORMANTS)

columns = all_vowels_formants_org_synth_df.columns
new_cols = [
    "rir_type",
    "f1_praat_rvb_mean",
    "f2_praat_rvb_mean",
    "f3_praat_rvb_mean",
    "f1_praat_rvb_std",
    "f2_praat_rvb_std",
    "f3_praat_rvb_std",
]

columns = np.concatenate([columns, new_cols])

FS = 16000
DUR = 2
CHUNK_DUR = DUR / 3

rir_signals = {
    (p.replace("RVB2014_type1_rir_", "").replace(".wav", "")): librosa.load(
        join(RIR_SIGNAL_PATH, p), sr=FS
    )[0]
    for p in os.listdir(RIR_SIGNAL_PATH)
}

dfs_list = np.array_split(all_vowels_formants_org_synth_df, 8)


def distort(aud_sig, rir_sig):
    rir_sig = rir_sig[: len(rir_sig) // 15]
    out_len = len(aud_sig) + len(rir_sig) - 1
    aud_sig_fft = fft(aud_sig, n=out_len)
    rir_sig_fft = fft(rir_sig, n=out_len)
    aud_sig_reverb = np.real(ifft(np.multiply(aud_sig_fft, rir_sig_fft)))[
        : len(aud_sig)
    ]
    aud_sig_reverb = aud_sig_reverb / max(abs(aud_sig_reverb))

    return aud_sig_reverb


def export_formants(df: pd.DataFrame):

    rvb_formants = []
    N_VOWEL_INSTANCES = len(df)
    split_id = df.iloc[0, :]["id"]
    ALL_ORG_SYN_RVB_FORMANTS = f"all_vowels_formants_org_synth_rvb_{split_id}.csv"
    TMP_RVB_FOLDER = f"/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/tmprvb_{split_id}"

    for i in range(N_VOWEL_INSTANCES):

        vow = df.iloc[i, :]

        fname_aud = vow["filename"]
        fpath_aud = join(ALL_SYNTH_VOWEL_PATH, f"{fname_aud}.wav")

        if os.path.exists(TMP_RVB_FOLDER):
            shutil.rmtree(TMP_RVB_FOLDER)

        os.mkdir(TMP_RVB_FOLDER)

        # reverb
        sig_aud = librosa.load(fpath_aud, sr=FS)[0]
        for rir_typ in rir_signals.keys():
            sig_aud_rvb = distort(sig_aud, rir_signals[rir_typ])

            fname_aud_rir = f"{fname_aud}_rvb_{rir_typ}.wav"
            fpath_aud_rir = join(TMP_RVB_FOLDER, fname_aud_rir)

            sf.write(fpath_aud_rir, sig_aud_rvb, FS)

            formants = pfp.formants_at_interval(
                fpath_aud_rir,
                CHUNK_DUR,
                CHUNK_DUR * 2,
                maxformant=5500,
                winlen=0.025,
                preemph=50,
            )

            fm_mean = formants.mean(axis=0)[1:]
            fm_std = formants.std(axis=0)[1:]

            info = vow.values.tolist()
            rvb_formants.append(np.concatenate([info, [rir_typ], fm_mean, fm_std]))

    columns = df.columns
    new_cols = [
        "rir_type",
        "f1_praat_rvb_mean",
        "f2_praat_rvb_mean",
        "f3_praat_rvb_mean",
        "f1_praat_rvb_std",
        "f2_praat_rvb_std",
        "f3_praat_rvb_std",
    ]
    columns = np.concatenate([columns, new_cols])

    rvb_formants_df = pd.DataFrame(rvb_formants, columns=columns)

    columns_arrange = [
        "id",
        "filename",
        "phone",
        "pitch",
        "rir_type",
        "f1_org_praat",
        "f2_org_praat",
        "f3_org_praat",
        "f1_praat_synth_mean",
        "f2_praat_synth_mean",
        "f3_praat_synth_mean",
        "f1_praat_synth_std",
        "f2_praat_synth_std",
        "f3_praat_synth_std",
        "f1_praat_rvb_mean",
        "f2_praat_rvb_mean",
        "f3_praat_rvb_mean",
        "f1_praat_rvb_std",
        "f2_praat_rvb_std",
        "f3_praat_rvb_std",
    ]
    rvb_formants_df = rvb_formants_df[columns_arrange]
    rvb_formants_df.index.name = "slno"
    rvb_formants_df.to_csv(ALL_ORG_SYN_RVB_FORMANTS, index=True)


if __name__ == "__main__":
    for d in dfs_list:
        p = Process(target=export_formants, args=(d,))
        p.start()
        # p.join()
