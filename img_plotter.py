import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys, os
import datetime as dt

sample_rate = 512 # Hz
seconds = 60 # seconds to plot
samples_to_plot = seconds * sample_rate

# just putting one of the files here as a variable so I can use it in the function to
# test the function
folder = '/home/ursa/ccom/REU2022/IMU_Data/2022-07-26_14.40.36_AudioIMUMiki_SD_MickyAvi'
csv_file = os.path.abspath('./IMU_Data/2022-07-26_14.40.36_AudioIMUMiki_SD_MickyAvi/AudioIMUMiki_Session1_Shimmer_60F7_Calibrated_SD.csv')


        
        
def plot(csv_file):
    
    df = pd.read_csv(csv_file, sep='\t', skiprows=[0,2])
    # print row
    # print(type(df.iloc[0][0]))
    
    # plot the entire dataframe
    # calculate magnitude of the acceleration data
    # skip row
    df['Magnitude'] = np.sqrt(df['Shimmer_60F7_Accel_WR_X_CAL']**2 + df['Shimmer_60F7_Accel_WR_Y_CAL']**2 + df['Shimmer_60F7_Accel_WR_Z_CAL']**2)

    y  = df['Magnitude']
    #convert timestamp to datetime
    # time stampt format is 'YYYY/MM/DD HH:MM:SS.SSS'
    format = '%Y/%m/%d %H:%M:%S.%f'
    df['Shimmer_60F7_Timestamp_FormattedUnix_CAL'] = pd.to_datetime(df['Shimmer_60F7_Timestamp_FormattedUnix_CAL'], format=format)
    
    x = df['Shimmer_60F7_Timestamp_FormattedUnix_CAL']


    if not os.path.exists('./Images'):
        os.mkdir('./Images')
    
    # 737280/30720 = 24, 24 minutes of data
    # 512 samples per second, 1 sec = 512, 2 sec = 512 x 2, 60secs = 512 x 60   
    # minute_samples = 30720
    # 24 chunks

    iterator = 30720
    iteration = 0
    x = [x[i:i+iterator] for i in range(0, len(x), iterator)]
    y = [y[i:i+iterator] for i in range(0, len(y), iterator)]

    plots = zip(x,y)
    def loop_plot(plots):
        figs={}
        axs={}
        for idx,plot in enumerate(plots):
            figs[idx]=plt.figure()
            # increase plot size
            figs[idx].set_size_inches(10,10)
            axs[idx]=figs[idx].add_subplot(111)
            axs[idx].plot(plot[0],plot[1])
            figs[idx].savefig("./Images/MikiAvi/plot_%s.png" %idx)
            # close figure
            plt.close(figs[idx]) 
    loop_plot(plots)

plot(csv_file)



        



