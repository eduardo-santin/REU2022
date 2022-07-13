import json
import pandas as pd 
import os,sys 
import json
import numpy as np

file = os.path.abspath('./ontology.json')

# open the json file and load the data
with open(file) as f:
    data = json.load(f)
    
    # open a dataframe to store the data
    df = pd.DataFrame(columns=['name','id'])

    #create a list to store the data of name and id
    name = []
    id = []
    # add data to the list
    for i in data:
        name.append(i['name'])
        id.append(i['id'])
    # add the list to the dataframe
    df = pd.concat([df,pd.DataFrame({'name':name,'id':id})])

    #save the dataframe to a xlsx file
    df.to_excel('ontology.xlsx', index=False, engine='openpyxl')

