import os, sys, shutil


def separate_audio_to_folder(save_folder, data_folder = 'New_Data'):
    folder = os.path.abspath(data_folder)

    # if it doesn't exist create new folder for the audio files
    if not os.path.exists('./Annotated_Data2'):
        os.mkdir('./Annotated_Data2')
    if not os.path.exists('./Annotated_Data2/Audio_Data'):
        os.mkdir('./Annotated_Data2/Audio_Data')
    if not os.path.exists('./Annotated_Data2/WAV_Data'):
        os.mkdir('./Annotated_Data2/WAV_Data')
      # create folder for indicated person
    if not os.path.exists('./Annotated_Data2/Audio_Data/' + save_folder):
        os.mkdir('./Annotated_Data2/Audio_Data/' + save_folder)
    if not os.path.exists('./Annotated_Data2/WAV_Data/' + save_folder):
        os.mkdir('./Annotated_Data2/WAV_Data/' + save_folder)
    audiofolder = os.path.abspath('./Annotated_Data2/Audio_Data/' + save_folder)  

    for files in os.listdir(folder):
        #moving the files to the new folder
        if files.endswith('.3gpp'):
            print('Moving ' + files + ' to folder...')
            shutil.copy(folder + '/' + files, audiofolder)
            




def create_wav(origin_folder, save_folder):
    print('\nCreating wav files...')
    print('Origin folder: ' + origin_folder)
    for files in os.listdir(origin_folder):
        # if file already exists, skip it
        file = files.replace('.3gpp', '.wav')
        if os.path.exists(save_folder + '/' + file):
            continue
        # convert the files to wav
        #hide ffmpeg banner
        os.system('ffmpeg' + ' -hide_banner ' + ' -i ' + origin_folder + '/' + files + ' ' + save_folder + '/' + files.split('.')[0] + '.wav')
        



# make sure a sys argument is passed in
if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
    print('Missing folder path or not a folder')
    
    sys.exit()

folder = sys.argv[1] + '/' + sys.argv[2]
# make sure second directory is passed in
if len(sys.argv) < 3 or not os.path.isdir(folder):
    print('Missing folder path or not a folder 2')
    
    sys.exit()


separate_audio_to_folder(sys.argv[2], folder)
create_wav('./Annotated_Data2/Audio_Data/' + sys.argv[2], './Annotated_Data2/WAV_Data/' + sys.argv[2])
