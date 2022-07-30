import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import os



csv_file = os.path.abspath('./IMU_Data/2022-07-26_14.40.36_AudioIMUMiki_SD_MickyAvi/AudioIMUMiki_Session1_Shimmer_60F7_Calibrated_SD.csv')




def plot(csv_file):
    # input start time and end time

    df = pd.read_csv(csv_file, sep='\t', skiprows=[0,2])
    # find the index of the start time
    start_index = 1
    # find the index of the end time
    end_index = 1
    
    activity = input('Enter activity: ')
    person = input('Enter person: ')


    x = df['Shimmer_60F7_Timestamp_FormattedUnix_CAL'][start_index:end_index]
    y = df['Magnitude'][start_index:end_index]
    plt.plot(x,y)
    plt.title(activity)
    plt.xlabel('Time')
    plt.ylabel('Magnitude')
    # save the plot
    plt.savefig('./Images/MikiAvi/%s_%s_found.png' %(person, activity))