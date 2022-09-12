#!/home/jeevan/dev/anaconda3/envs/pytorch/bin/python

import os
import pandas as pd
from os.path import join
import librosa
import numpy as np
from scipy.fft import fft, ifft
import soundfile as sf
from tqdm import tqdm
import praat_formants_python.praat_formants_python as pfp


ALL_SYNTH_VOWEL_PATH = "/home/jeevan/projects/Asquire/Formants/tmpexp"
RIR_SIGNAL_PATH = "/home/jeevan/projects/Asquire/Formants/rir_data"
ALL_TIMIT_VOWEL_CSV = "/home/jeevan/projects/Asquire/Formants/all_timit_vowel_formants.csv"
TMP_RVB_FOLDER = "/home/jeevan/projects/Asquire/Formants/tmprvb"

FS = 16000

DUR = 2
CHUNK_DUR = DUR/3

rir_signals = {(p.replace("RVB2014_type1_rir_", "").replace(".wav", "")): librosa.load(join(RIR_SIGNAL_PATH, p), sr=FS)[0] for p in os.listdir(RIR_SIGNAL_PATH)}


for id, vow in tqdm(all_vowels_df.iterrows()):

    phn, uid, pth = (vow["phone"], vow["id"], vow["pitch"])
    fname_aud = f"{phn}_{uid}_{pth}.wav"
    fpath_aud = join(ALL_SYNTH_VOWEL_PATH, fname_aud)

    

    #reverb
    sig_aud = librosa.load(fpath_aud , sr=FS)[0]
    for k in rir_signals.keys():
        sig_aud_rvb = distort(sig_aud, rir_signals[k])
        fname_aud_rir = f"{phn}_{uid}_{pth}_rvb_{k}.wav"
        fpath_aud_rir = join(TMP_RVB_FOLDER, fname_aud_rir)
        
        print(fpath_aud_rir)

        sf.write(fpath_aud_rir, sig_aud_rvb, FS)
        
        break


    print(fpath_aud, os.path.exists(fpath_aud))

    break

def distort(aud_sig, rir_sig):
    rir_sig = rir_sig[: len(rir_sig) // 15]
    out_len = len(aud_sig) + len(rir_sig) - 1
    aud_sig_fft = fft(aud_sig, n=out_len)
    rir_sig_fft = fft(rir_sig, n=out_len)
    aud_sig_reverb = np.real(ifft(np.multiply(aud_sig_fft, rir_sig_fft)))[: len(aud_sig)]
    aud_sig_reverb = aud_sig_reverb / max(abs(aud_sig_reverb))

    return aud_sig_reverb


synth_vowels = [join(ALL_SYNTH_VOWEL_PATH, p) for p in os.listdir(ALL_SYNTH_VOWEL_PATH)]

synth_formants = []
for p in tqdm(synth_vowels):

    sig_aud = librosa.load(fpath_aud , sr=FS)[0]
    for k in rir_signals.keys():
        sig_aud_rvb = distort(sig_aud, rir_signals[k])
        fname_aud_rir = f"{phn}_{uid}_{pth}_rvb_{k}.wav"
        fpath_aud_rir = join(TMP_RVB_FOLDER, fname_aud_rir)
        
        print(fpath_aud_rir)

        sf.write(fpath_aud_rir, sig_aud_rvb, FS)
        
        break

    formants = pfp.formants_at_interval(p, CHUNK_DUR, CHUNK_DUR * 2, 
                                        maxformant=5500, winlen=0.025, preemph=50)

    name = os.path.basename(p).replace(".wav", "")
    phn, pitch, id = name.split("_")

    info = [id, name, phn, pitch]

    fm_mean = formants.mean(axis=0)[1:]
    fm_std = formants.std(axis=0)[1:]

    # print(formants)
    synth_formants.append(np.concatenate([info, fm_mean, fm_std]))

    # break

columns=["id", "filename", "phone", "pitch", "f1_praat_synth_mean", "f2_praat_synth_mean","f3_praat_synth_mean","f1_praat_synth_std","f2_praat_synth_std","f3_praat_synth_std"]
synth_formants_df = pd.DataFrame(synth_formants, columns=columns)
synth_formants_df.to_csv("synth_vowel_formants_praat.csv", index=False)