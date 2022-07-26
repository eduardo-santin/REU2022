import os, sys


def separate_audio_to_folder(data_folder = 'New_Data'):
    folder = os.path.abspath(data_folder)

    # if it doesn't exist create new folder for the audio files
    if not os.path.exists('./Annotated_Data2') or not os.path.exists('./Annotated_Data2/Audio_Data'):
        os.mkdir('./Annotated_Data2/Audio_Data')
        os.mkdir('./Annotated_Data2/WAV_Data')
    annotated_folder = os.path.abspath('./Annotated_Data2/Audio_Data')  

    for files in os.listdir(folder):
        #copy the files to the annotated folder
        if files.endswith('.3gpp'):
            os.system('cp ' + folder + '/' + files + ' ' + annotated_folder)




def create_wav(origin_folder, save_folder):
    print('Creating wav files...')
    print('Origin folder: ' + origin_folder)
    for files in os.listdir(origin_folder):
        # if file already exists, skip it
        file = files.replace('.3gpp', '.wav')
        if os.path.exists(save_folder + '/' + file):
            continue
        # convert the files to wav
        print('Converting ' + files + ' to wav...')
        os.system('ffmpeg -i ' + origin_folder + '/' + files + ' ' + save_folder + '/' + files.split('.')[0] + '.wav')
        



# make sure a sys argument is passed in
if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
    print('Missing folder path or not a folder')
    sys.exit()

separate_audio_to_folder(sys.argv[1])
create_wav('./Annotated_Data2/Audio_Data', './Annotated_Data2/WAV_Data')
