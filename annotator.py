import os
import sys
import pandas as pd
import numpy as np
# import time, calendar

# dictionary of activities
activities = {
    'sitting': '1',
    'walking': '3',
    'standing': '2',
    'stairs': '4',
}

def annotate(data_folder):
    folder = os.path.abspath(folder)

    # if it doesn't exist create new folder for annotated data
    if not os.path.exists('./Annotated_Data'):
        os.mkdir('./Annotated_Data')
    annotated_folder = os.path.abspath('./Annotated_Data')  

    for files in os.listdir(folder):
        #For the data recorded from the esense device
        if files.endswith('.xls'):
            df = pd.read_excel(folder + '/' + files)

            # label the columns
            df.columns = ['time', 'Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz', 'Activity Label', 'Activity']
            # delete the first and second row
            df = df[2:]


            # grab the first word of the file name so we can label
            # the dataframe with the activity
            activity = files.split('_')[0]

            # add a column for the activity at the end of the dataframe 
            # and fill it with the activity label
            df['Activity'] = activity.capitalize()
    
            # depending on the activity, we change the 
            # activity label to the corresponding number
            # from our dictionary
            if activity == 'staying':
                df['Activity Label'] = activities['sitting']

            elif activity == 'walking':
                df['Activity Label'] = activities['walking']

            elif activity == 'standing':
                df['Activity Label'] = activities['standing']

            elif activity == 'stairs':
                df['Activity Label'] = activities['stairs']


            # The recording for sitting and standing was done with the same
            # label in the esense app since the phone app did not have a different
            # label for the sitting and standing activities.
            # The standing recordings were renamed accordingly instead
            # of the sitting recordings. So to fix this all esense files starting
            # with staying are renamed to sitting to avoid confusion due to my mistake.
            if activity == 'staying':
                df.to_csv(annotated_folder + '/' + files.replace('staying', 'sitting') + files.replace('.xls', '_esense.csv'), index=False, encoding='utf-8')

            
            
            # save the dataframe to a csv, writing esense on the end
            # to have some clear distinction between the two dataframes
            df.to_csv(annotated_folder + '/' + files.replace('.xls', '_esense.csv'), index=False, encoding='utf-8')


        #For the data recorded on the smartphone app
        if files.endswith('.csv'):
            df = pd.read_csv(folder + '/' + files)

            # grab the first word of the file name so we can label
            # the dataframe with the activity
            activity = files.split(' ')[0]


            if activity == 'sitting':
                df['Activity Label'] = activities['sitting']

            elif activity == 'walking':
                df['Activity Label'] = activities['walking']

            elif activity == 'standing':
                df['Activity Label'] = activities['standing']

            elif activity == 'stairs':
                df['Activity Label'] = activities['stairs']



            # add a column for the activity at the end of the dataframe 
            # and fill it with the activity label
            df['Activity'] = activity.capitalize()
    
            # save the dataframe to a csv, writing phone on the end
            # to have some clear distinction between the two dataframes
            df.to_csv('./Annotated_Data/' + files.replace('.csv', '_phone.csv'), index=False, encoding='utf-8')
        

# Somewhat unfinished, need to discuss this more.
# Will cut the dataframe using the sampling rate found in the jave code
# and found in the accelerometer phone app accordingly
def cut_audio(default_time = 30, folder = './Annotated_Data'):
    
    # iterate through the annotated folder and cut the files so the time is the same

    # calculate how many rows we have to cut by multiplying the seconds with sample rate
    # sample rate for the esense is 50Hz
    # sample rate for the phone recordings are 421Hz
    esense_sample_rate = 50
    phone_sample_rate = 421



    for files in os.listdir(folder):
        if files.endswith('_esense.csv'):
            # read the csv file

            df = pd.read_csv(folder + '/' + files)

            # grab the first time stamp and the last time stamp

            first_time = df['time stamps'].iloc[0]
            last_time = df['time stamps'].iloc[-1]

            # calculate the difference between the first and last time stamp to
            # figure the duration of the audio

            duration = last_time - first_time
            # calculate how much we need to cut by getting the
            # remainder of the duration and the default time

            cut_amount = duration - default_time

            # calculate how many samples we need to cut by multiplying 
            # the cut amount with the sample rate
            cut_amount_samples = cut_amount * esense_sample_rate

            # divide the cut amount of samples to 
            # shave off the start and end of the audio

            # if the duration is a odd number, we shave off more on the end
            if duration % 2 == 1:
                start_cut = cut_amount_samples // 2
                end_cut = (cut_amount_samples // 2) + 1
            else:
                start_cut = cut_amount_samples // 2
                end_cut = cut_amount_samples // 2

            # cut the the columns of the dataframe
            df = df[start_cut:-end_cut]
            
            # save the dataframe to a csv
            df.to_csv(folder + '/' + files.replace('_esense.csv', '_esense_cut.csv'), index=False, encoding='utf-8')

        if files.endswith('_phone.csv'):
            # read the csv file

            df = pd.read_csv(folder + '/' + files)

            # grab the last time stamp since the
            # phone recordings are timed in seconds with milliseconds
            last_time = df['time'].iloc[-1]

            #calculate how much to cut with the default time
            cut_amount = last_time - default_time

            # divide the cut amount of samples to 
            # shave off the start and end of the audio
            # if the duration is a odd number, we shave off more on the end
            if duration % 2 == 1:
                start_cut = cut_amount_samples // 2
                end_cut = (cut_amount_samples // 2) + 1
            else:
                start_cut = cut_amount_samples // 2
                end_cut = cut_amount_samples // 2

            # cut the the columns of the dataframe
            df = df[start_cut:-end_cut]

            # save the dataframe to a csv
            df.to_csv(folder + '/' + files.replace('.csv', '_cut.csv'), index=False, encoding='utf-8')



# make sure a sys argument is passed in
if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
    print('Missing folder path or not a folder')
    sys.exit()

annotate(sys.argv[1])
