# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 15:43:48 2022

@author: Spirelab
"""

import IPython
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from tqdm import tqdm
import os
from scipy.io.wavfile import write
import scipy.signal
from spectrum import aryule
from pylab import plot, axis, xlabel, ylabel, grid, log10
import scipy.signal
from nara_wpe.wpe import wpe
from nara_wpe.wpe import get_power
from nara_wpe.utils import stft, istft, get_stft_center_frequencies
from nara_wpe import project_root
import os
import librosa

def data_acq() : 
    D,T = 1,10000
    y = np.random.normal(size = (D,T))
    return y

os.chdir('/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/')

channels = 1

sampling_rate = 16000

delay = 3

iterations = 5

taps = 10

alpha=0.9999

y = data_acq()

Y = stft(y, size = 512 , shift = 128)

Y1 = Y.transpose(2,0,1)

Z = wpe(Y1)

z_np = istft(Z.transpose(1,2,0), size = 512, shift = 128)

channels = 8

sampling_rate = 16000

delay = 3

iterations = 5

taps = 10

alpha = 0.999

audio_file, _ = librosa.load('/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/iy_19593_179_rvb_largeroom1_far_angla.wav' , sr = None)

audio_file = audio_file.transpose()

tmp = np.broadcast_to(audio_file, [1, len(audio_file)])

Y_tmp = stft(tmp , size = 512, shift = 128)

Y_tmp = Y_tmp.transpose(2,0,1)

Z_tmp = wpe(Y_tmp)

Z_tmp = Z_tmp.transpose(1,2,0)

z_tmp = istft(Z_tmp, size = 512 , shift = 128)

z_tmp.transpose()[0:3] = 0

IPython.display.Audio(z_tmp[0], rate=sampling_rate)

#librosa.output.write_wav('C:/Users/Spirelab/Desktop/Vowel_Triangle/Deverb_Algos/nara_wpe/drv.wav', z_tmp, sr = sampling_rate)

sf.write('/home/jeevan/Jeevan_K/Projects/Asquire/Reverb-Quest/Formants/drv.wav', z_tmp , 16000)

#write('drv.wav', 16000 , z_tmp)

#for plotting images

fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(20, 10))

im1 = ax1.imshow(20 * np.log10(np.abs(Y_tmp[ :, 0, 200:400])), origin='lower')

ax1.set_xlabel('frames')

_ = ax1.set_title('reverberated')

im2 = ax2.imshow(20 * np.log10(np.abs(Z_tmp[0, 200:400, :])).T, origin='lower', vmin=-120, vmax=0)

ax2.set_xlabel('frames')

_ = ax2.set_title('dereverberated')

cb = fig.colorbar(im2)


