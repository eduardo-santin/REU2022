import os, sys, hashlib
from re import A
import pandas as pd
import numpy as np
# import time, calendar

# dictionary of activities
activities = {
    'Typing': 1,
    'Drawer': 2,
    'Knocking': 3,
    'Chopping': 4,
    'Walking': 5, 
}


# easier to just download the data from the drive and 
# elimanate the duplicate files.
# made this because ill have 1 or 2 duplicates of the same file
def elim_dupes(data_folder = 'Data'):
    folder = os.path.abspath(data_folder)
    # check for duplicate files
    print('removing duplicates...')

    # check if the file
    for files in os.listdir(folder):
        if ( (files.endswith(').xls') or files.endswith(').xls'))
            or (files.endswith(').csv') or files.endswith(').csv'))
            or (files.endswith(').3gpp') or files.endswith(').3gpp')) ):
            os.remove(folder + '/' + files)
            print('Deleted ' + files)
            # delete the files




def annotate(save_folder, data_folder = 'New_Data'):
    folder = os.path.abspath(data_folder)

    # if it doesn't exist create new folder for annotated data
    if not os.path.exists('./Annotated_Data2'):
        os.mkdir('./Annotated_Data2')
    # create folder for the csv files
    if not os.path.exists('./Annotated_Data2/CSV_Data'):
        os.mkdir('./Annotated_Data2/CSV_Data')
    
    # create folder for indicated person
    if not os.path.exists('./Annotated_Data2/CSV_Data/' + save_folder):
        os.mkdir('./Annotated_Data2/CSV_Data/' + save_folder)
        
    annotated_folder = os.path.abspath('./Annotated_Data2/CSV_Data/' + save_folder)
    
    # sometimes the esense earable disconnects
    # right before recording or it does not update the visualizer that it's disconnected
    # so just for ease of use, collect all the empty files and delete them
    empty_files = []

    print('Annotating files...')
    for files in os.listdir(folder):
        #For the data recorded from the esense device
        

        if files.endswith('.xls'):
            # grab the first word of the file name so we can label
            # the dataframe with the activity
            activity = files.split('_')[0]
            activity = activity.capitalize()
            # print('entre')
            print(activity)

            
            df = pd.read_excel(folder + '/' + files, engine='xlrd')

            if df.empty:
                print(files + ' is empty')
                # collect the file name in a list
                empty_files.append(files)
                continue


            # label the columns
            df.columns = ['time', 'ax', 'ay', 'az', 'wx', 'wy', 'wz', 'activity Label', 'activity']
            # delete the first and second row
            df = df[2:]

            # subtract the unix timestamp from the start time to get how long between the start and end of the recording
            df['time'] = df['time'] - df['time'].iloc[0]
            # convert the time to seconds
            df['time'] = df['time'] / 1000


    
            # depending on the activity, we change the 
            # activity label to the corresponding number
            # from our dictionary
            df['activity Label'] = activities[activity]

            # add a column for the activity at the end of the dataframe 
            # and fill it with the activity label
            df['activity'] = activity
            

            files = save_folder + '_' + files
            
            # print('saving ' + files)
            # add name to the start of the file name
            df.to_csv(annotated_folder+ '/' + files.replace('.xls', '_esense.csv'), index=False, encoding='utf-8')


        #For the data recorded on the smartphone app
        if files.endswith('.csv'):
            df = pd.read_csv(folder + '/' + files)


            if df.empty:
                print(files + ' is empty')
                # collect the file name in a list
                empty_files.append(files)
                continue


            # grab the first word of the file name so we can label
            # the dataframe with the activity
            activity = files.split(' ')[0]
            activity = activity.capitalize()

            # if they have an unnamed column, delete it
            if 'Unnamed: 7' in df.columns:
                df.drop(columns='Unnamed: 7', inplace=True)

            if activity == 'Sitting':
                df['activity Label'] = activities['Sitting']

            elif activity == 'Walking':
                df['activity Label'] = activities['Walking']

            elif activity == 'Standing':
                df['activity Label'] = activities['Standing']

            elif activity == 'Stairs':
                df['activity Label'] = activities['Stairs']



            # add a column for the activity at the end of the dataframe 
            # and fill it with the activity label
            df['activity'] = activity
    
            # save the dataframe to a csv, writing phone on the end
            # to have some clear distinction between the two dataframes
            df.to_csv(annotated_folder + '/' + files.replace('.csv', '_phone.csv'), index=False, encoding='utf-8')
        
    # ask the user if they want to delete all empty files
    if len(empty_files) > 0:
        delete = input('\nDo you want to delete all empty files? (y/n) ')
        if delete == 'y':
            print('/n')
            for files in empty_files:
                os.remove(folder + '/' + files)
                print('Deleted ' + files)


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
            # df.to_csv(save + '/' + files.replace('_esense.csv', '_esense_cut.csv'), index=False, encoding='utf-8')

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

folder = sys.argv[1] + '/' + sys.argv[2]
# make sure second directory is passed in
if len(sys.argv) < 3 or not os.path.isdir(folder):
    print('Missing folder path or not a folder 2')
    
    sys.exit()

elim_dupes()
annotate(sys.argv[2], folder)


