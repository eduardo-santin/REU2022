import os, sys


def separate_audio_to_folder(data_folder = 'Data'):
    folder = os.path.abspath(data_folder)

    # if it doesn't exist create new folder for the audio files
    if not os.path.exists('./Annotated_Data') or not os.path.exists('./Annotated_Data/Audio_Data'):
        os.mkdir('./Annotated_Data/Audio_Data')
    annotated_folder = os.path.abspath('./Annotated_Data/Audio_Data')  

    for files in os.listdir(folder):
        #copy the files to the annotated folder
        if files.endswith('.3gpp'):
            os.system('cp ' + folder + '/' + files + ' ' + annotated_folder)

# make sure a sys argument is passed in
if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
    print('Missing folder path or not a folder')
    sys.exit()

separate_audio_to_folder(sys.argv[1])
