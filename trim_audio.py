import numpy
import scipy.io.wavfile as wav
import os, sys
import numpy as np
import matplotlib.pyplot as plt


def cut_audio(cut_time, name, file_path):
    # open the wav file
    sample_rate, audio_data = wav.read(file_path)
    # get the amount of samples to cut
    cut_amount_samples = cut_time * sample_rate
    # remove the samples from the start of the audio
    audio_data = audio_data[cut_amount_samples:]
    # graph the new audio
    duration = len(audio_data)/sample_rate
    time = np.arange(0,duration,1/sample_rate) #time vector



    plt.xlim(0, duration)
    plt.plot(time, audio_data)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    plt.savefig('./Graph_Data2/Audio/' + name + '/New_images/' + file_path.split('/')[-1]+ '.png')
    plt.close()


    
    


    
cut_audio(int(sys.argv[1]), sys.argv[2], sys.argv[3])