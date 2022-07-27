import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os, sys
# import wave
import datetime
import scipy.io.wavfile as wav


def graph_audio(folder, name):
    for files in os.listdir(folder):
        #graph the wav file
        wavedata = os.path.join(folder, files)
        sampleRate, audioBuffer = wav.read(wavedata)
        duration = len(audioBuffer)/sampleRate

        time = np.arange(0,duration,1/sampleRate) #time vector

        # limit the x axis to the duration of the audio file
        plt.xlim(0, duration)
        plt.plot(time,audioBuffer)
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.title(files.split('.')[0])
        # data = wav.readframes(wav.getnframes())
        # data = np.frombuffer(data, dtype=np.int16)
        # # label the x-axis
        # x = np.linspace(0, len(data), len(data))
        # plt.xlabel('Time (s)')

        # #label the y-axis
        # y = data
        # plt.ylabel('Amplitude')

        # #make the x and y axis cap at the max and min values
        # plt.xlim(0, len(data))
        # plt.ylim(min(data), max(data))

        # # title the graph with the file name
        # plt.title(file.split('.')[0])
        # plt.plot(x, y)
        # save the graph
        plt.savefig('./Graph_Data2/Audio/' + name + '/' + files.split('.')[0] + '.png')
        # close the graph
        plt.close()
        
def graph_csv(folder, name):
    for file in os.listdir(folder):
        # get the data from the csv file
        data = pd.read_csv(folder + '/' + file)
        # make subplot to accomadate 2 graphs
        fig, ax = plt.subplots(2, 1)

        # increase figure size
        fig.set_size_inches(15, 10)
    

        #plot for acelerometer data
        #set the x and y axis labels,title, and limits
        ax[0].set_xlabel('Time (s)')
        ax[0].set_ylabel('Acceleration (m/s^2)')
        ax[0].set_title(file.split('.')[0] + ' Acceleration')
        ax[0].set_xlim(0, max(data['time']))
        # convert unix milliseconds to regular time
        # if data['time'].dtype == 'float64':
        #     data['time'] = data['time'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000))
        # # the limit of the y axis is set to the max and min values of the ax, ay, and az columns
        # I keep getting errors any other form of writing this so im just doing it this way
        min_ax = min(data['ax'])
        max_ax = max(data['ax'])
        min_ay = min(data['ay'])
        max_ay = max(data['ay'])
        min_az = min(data['az'])
        max_az = max(data['az'])
        ax[0].set_ylim(min(min_ax, min_ay, min_az), max(max_ax, max_ay, max_az))

        #plot the data from the 3 columns of the csv file
        ax[0].plot(data['time'], data['ax'], label = 'X')
        ax[0].plot(data['time'], data['ay'], label = 'Y')
        ax[0].plot(data['time'], data['az'], label = 'Z')
        ax[0].legend()

        #plot for gyroscope data
        ax[1].set_xlabel('Time (s)')
        ax[1].set_ylabel('Angular Velocity (rad/s)')
        ax[1].set_title(file.split('.')[0] + ' Gyroscope')
        ax[1].set_xlim(0, max(data['time']))
        min_wx = min(data['wx'])
        max_wx = max(data['wx'])
        min_wy = min(data['wy'])
        max_wy = max(data['wy'])
        min_wz = min(data['wz'])
        max_wz = max(data['wz'])
        ax[1].set_ylim(min(min_wx, min_wy, min_wz), max(max_wx, max_wy, max_wz))
        ax[1].plot(data['time'], data['wx'], label = 'X')
        ax[1].plot(data['time'], data['wy'], label = 'Y')
        ax[1].plot(data['time'], data['wz'], label = 'Z')
        ax[1].legend()
        # save the graph
        plt.savefig('./Graph_Data2/CSV/' + name + '/' + file.split('.')[0] + '.png')
        # close the graph
        plt.close()


        





def create_graphs(save_folder, data_folder = 'New_Data'):
    folder =  os.path.abspath(data_folder)

    #create directory and subdirectories if they don't exist
    if not os.path.exists('./Graph_Data2'):
        os.mkdir('./Graph_Data2')
        # make subdirectories for audio and csv files
        os.mkdir('./Graph_Data2/Audio')
        os.mkdir('./Graph_Data2/CSV')
    # create folder for indicated person
    if not os.path.exists('./Graph_Data2/Audio/' + save_folder):
        os.mkdir('./Graph_Data2/Audio/' + save_folder)
    if not os.path.exists('./Graph_Data2/CSV/' + save_folder):
        os.mkdir('./Graph_Data2/CSV/' + save_folder)
        
    
        
    
    audio_data_folder = os.path.abspath('./Annotated_Data2/WAV_Data/' + save_folder)
    csv_data_folder = os.path.abspath('./Annotated_Data2/CSV_Data/' + save_folder)

    print('Creating graphs for audio data...')
    graph_audio(audio_data_folder, save_folder)
    print('Creating graphs for csv data...')
    graph_csv(csv_data_folder, save_folder)


# make sure a sys argument is passed in
if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
    print('Missing folder path or not a folder')
    
    sys.exit()

folder = sys.argv[1] + '/' + sys.argv[2]
# make sure second directory is passed in
if len(sys.argv) < 3 or not os.path.isdir(folder):
    print('Missing folder path or not a folder 2')
    
    sys.exit()


create_graphs(sys.argv[2], folder)
