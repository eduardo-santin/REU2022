import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import wave

from requests import head


def graph_audio(folder ):
    for file in os.listdir(folder):
        #temporarily convert 3gpp to wav
        os.system('ffmpeg -i ' + folder + '/' + file  + folder + '/' + file.split('.')[0] + '.wav')
        #graph the wav file
        wav = wave.open(folder + '/' + file.split('.')[0] + '.wav', 'r')
        data = wav.readframes(wav.getnframes())
        data = np.frombuffer(data, dtype=np.int16)
        # label the x-axis
        x = np.linspace(0, len(data), len(data))
        plt.xlabel('Time (s)')

        #label the y-axis
        y = data
        plt.ylabel('Amplitude')

        #make the x and y axis cap at the max and min values
        plt.xlim(0, len(data))
        plt.ylim(min(data), max(data))

        # title the graph with the file name
        plt.title(file.split('.')[0])
        plt.plot(x, y)
        # save the graph
        plt.savefig('./Graph_Data/Audio/' + file.split('.')[0] + '.png')
        # close the graph
        plt.close()
        # delete the wav file
        os.remove(folder + '/' + file.split('.')[0] + '.wav')

def graph_csv(folder):
    for file in os.listdir(folder):
        # get the data from the csv file
        data = pd.read_csv(folder + '/' + file)
        # the x-axis is the time of the recording
        x = data['Time']
        # the y-axis is the 


def create_graphs(data_folder = 'Data'):
    folder =  os.path.abspath(data_folder)

    #create directory and subdirectories if they don't exist
    if not os.path.exists('./Graph_Data'):
        os.mkdir('./Graph_Data')
        # make subdirectories for audio and csv files
        os.mkdir('./Graph_Data/Audio')
        os.mkdir('./Graph_Data/CSV')
    
    audio_data_folder = os.path.abspath('./Annotated_Data/Audio_Data')
    csv_data_folder = os.path.abspath('./Annotated_Data/CSV_Data')

    graph_audio(audio_data_folder)
    graph_csv(csv_data_folder)


# # make sure a sys argument is passed in
# if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
#     print('Missing folder path or not a folder')
#     sys.exit()

create_graphs()
