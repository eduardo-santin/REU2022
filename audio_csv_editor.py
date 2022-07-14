import os 
import pandas as pd
import json

# add all the decoded label names to the audio set csv file


# grab the ontology json file that has the label names
file = os.path.abspath('./ontology.json')

training_file = os.path.abspath('./balanced_train_segments.csv')

# open the csv file
#the first 3 lines are the header, so we skip them
df = pd.read_csv(training_file, header = 2, sep=', ', quotechar='"' , engine='python')

# make a list of the labels in the csv file
#there cn be multipel labels in one row, so we need to split them up
#and then make a list of all the labels
labels = set()
label_dict = {}

# loop through the rows in the csv file
for index, row in df.iterrows():
    # split the labels up
    labels_list = row['positive_labels'].strip('"').split(',')
    # add list items to the set
    labels.update(labels_list)
    
with open(file) as f:
    data = json.load(f)

    for i in data:
        if i['id'] in labels:
            label_dict[i['id']] = i['name']

# iterate through the dataframe and add a new column to the dataframe
# with the name of the labels in the postive_labels column

# create empty column
df['label_names'] = ''


for index, row in df.iterrows():
    # split the labels up
    labels_list = row['positive_labels'].strip('"').split(',')
    # create a new column in the dataframe
    for items in labels_list:
        # if the column is not empty, add a comma
        if df.at[index, 'label_names'] != '':
            df.at[index, 'label_names'] += ' | ' + label_dict[items]
        else:
            df.at[index, 'label_names'] = label_dict[items]

# save to csv
df.to_csv('experimental.csv', index=True)
