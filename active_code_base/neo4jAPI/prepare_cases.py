#realtor_graph.py


#from neo4j_connect_2 import NeoSandboxApp
#import neo4j_connect_2 as neo
#import GoogleServices as google
#from pyspark.sql import SparkSession
#from pyspark.sql.functions import struct
from cgitb import lookup
import code
from dbm import dumb
from doctest import master
from hmac import trans_36
import mimetypes
from platform import node
from pprint import pprint
from pty import master_open
from re import sub
from unittest.util import unorderable_list_difference
from urllib.parse import non_hierarchical
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, BooleanProperty, EmailProperty, Relationship,db)
import pandas as pd
#import NeoNodes as nn
#import GoogleServices
import neo4jClasses
#import sparkAPI as spark
import neoModelAPI as neo
import glob
import os
import json
import numpy as np
import re
#from neoModelAPI import NeoNodes as nn





    

def get_cwd():
    cwd = os.getcwd()
    return cwd

def get_files(cwd =os.getcwd(), input_directory = 'extras'):
    
    path = os.sep.join([cwd,input_directory])
    file_list= [f for f in glob.glob(path + "**/*.json", recursive=True)]
  
    return file_list

def instantiate_neo_model_api():
    uri = "7a92f171.databases.neo4j.io"
    user = "neo4j"
    psw = 'RF4Gr2IJTNhHlW6HOrLDqz_I2E2Upyh7o8paTwfnCxg'
    return neo.neoAPI.instantiate_neo_model_session(uri=uri,user=user,psw=psw)



def load_json_data(file):
    f = open (file, "r")
  
    # Reading from file
    data = json.loads(f.read())
    return data


def json_pipeline(file_list, master_subject_table):
    case_counter = 0
    for file in file_list:
        
        data = load_json_data(file=file)
        data = data['results']
        #pprint(data)
        #pprint(data[0])
        
        #filtered_data = filter_json_data(json_data = data, filter = filter)

        # Creating the case nodes transaction nodes and df
        data = clean_json_data(data)
        case_data = stringify_json_values(data)
        case_data = pandify_case_data(case_data)
        case_data = nodify_case_data(case_data = case_data)
        
        # Creating the subject nodes transaction nodes and df
        subject_list = slice_subject_data(data)
        subject_list = identify_unique_subjects(subject_list)
        subject_lookup_table = create_subject_lookup_table(subject_list)
        master_subject_table = integrate_to_master_table(subject_lookup_table,master_subject_table)
        #pprint(master_subject_table.duplicated())
        case_counter = case_counter + len(case_data)

        master_subject_table = nodify_subjects(master_subject_table)

        #pprint(case_data)
        #pprint(master_subject_table['transaction'])
        #lets save data to the database

        #master_subject_table = submit_subjects_to_db(master_subject_table)
        #case_data = submit_cases_to_db(case_data = case_data)

        # Create Relationships

        #relationship_list= create_relationship_table(case_data=case_data, master_subject_table=master_subject_table)
    




def submit_cases_to_db(case_data):
        #unsubmitted = master_subject_table[master_subject_table.notna()]

        ### in theory none of the cases wouldhave been submitted becasue i am pulling them from file.  There is no need to check.. Just submit
    #non_submitted_nodes = case_data[case_data['submitted'].isna()].copy()
    #pprint(non_submitted_nodes)
    ##pprint(non_submitted_nodes)
    #if non_submitted_nodes.empty:
    #    return case_data
    #else:
    case_data['transaction'] = case_data['transaction'].apply(lambda x: neo.neoAPI.update(x))
    #Assume all are submitted..
    case_data['submitted'] = True
    #test = non_submitted_nodes.iloc[32]['transaction']
    #return_obj = neo.neoAPI.update(test)
    #case_data.update(non_submitted_nodes)
    return case_data

    #Relationships must need to be created following saving to the df
    #relationships = create_relationship_table(case_data, master_subject_table)

def submit_subjects_to_db(master_subject_table):
    #unsubmitted = master_subject_table[master_subject_table.notna()]
    #pprint(master_subject_table)
    #non_submitted_nodes=master_subject_table[[master_subject_table['submitted'] == np.nan]]
    non_submitted_nodes = master_subject_table[master_subject_table['submitted'].isna()].copy()
    #pprint(non_submitted_nodes)
    if non_submitted_nodes.empty:   
        return master_subject_table
    else:
         #pprint(non_submitted_nodes)
        non_submitted_nodes['transaction'] = non_submitted_nodes['transaction'].apply(lambda x: neo.neoAPI.update(x))
        non_submitted_nodes['submitted'] = True
    
    #test = non_submitted_nodes.iloc[32]['transaction']
    #return_obj = neo.neoAPI.update(test)
        master_subject_table.update(non_submitted_nodes)
        #pprint(master_subject_table)
        return master_subject_table

def tester():
    return "Hello Dolly"

def create_relationship_table(case_data, master_subject_table):
    #pprint(case_data[])
        #test = master_subject_table['subject']
        # select 
    relationship_list = []
    for row in range(len(case_data)):
        unique_dataframe = (master_subject_table[master_subject_table['subject'].isin(case_data['subject_list'][row])])
        #pprint(unique_dataframe)
        for subject_row in range(len(unique_dataframe)):
            case = case_data.iloc[row]['transaction']
            subject = unique_dataframe.iloc[subject_row]['transaction']
            #create relationship
            #pprint(case)
            #pprint(subject)
            relationship = neo.neoAPI.create_relationship(case.subject_relationship,subject)
            #pprint(relationship)
            relationship_list.append(relationship)

    return relationship_list




        
    #create relationship between the case and each uid in the unique_data_frame_transaction_list 
    pprint(unique_dataframe)


    ## Creating the realation table

    # Thoughts
    # pass subject and case table
    # case_subject list collumn
    # where that list is in the master table
        #return  the subjects 
    # make a connection to between each subject and the case in the returned tableuid in the table
    # return a transaction list 
    # with the list commit a transaction for eachn 
    #

    #case_data= filter_case_data(data)
def nodify_case_data(case_data):
    #non_submitted_nodes = case_data[case_data.notna()]
    non_submitted_nodes = case_data[case_data.notna().any(axis=1)]
    #pprint(non_submitted_nodes)
    case_nodes = non_submitted_nodes.apply(lambda x :neo.neoAPI.create_case_node(date = x['date'], dates= x['dates'],group = x['group'], name=x['id'], pdf= x['pdf'], shelf_id = x['shelf_id'], subject= x['subject'], title = x['title'], url = x['url'], subject_relationship=True), axis=1)

    case_data['transaction'] = case_nodes
    return case_data




def filter_case_data(data):
    pprint(data[0])



def nodify_subjects(master_subject_table):
    non_submitted_nodes = master_subject_table[master_subject_table.isna().any(axis=1)].copy()
    #df[df.isna().any(axis=1)]
    #pprint(non_submitted_nodes)
    non_submitted_nodes['transaction'] = non_submitted_nodes['subject'].apply(lambda x :neo.neoAPI.create_subject_node(name = x))
    master_subject_table.update(non_submitted_nodes)
    return master_subject_table

def integrate_to_master_table(subject_lookup_table, master_subject_table):
    #check_if subject in list is in subject of the table
    # if so drop it from the temp table
    # append what is left to the master table 
    #pprint(subject_lookup_table)
    test = master_subject_table['subject']
    unique_dataframe = (subject_lookup_table[~subject_lookup_table['subject'].isin(test)])
    #pprint(unique_dataframe)
    #duplicate_list = (master_subject_table[~master_subject_table['subject'].isin(subject_lookup_table['subject'])])
    master_subject_table = pd.concat([master_subject_table,unique_dataframe])
    #master_subject_table.update(unique_dataframe)
    master_subject_table.reset_index(inplace=True, drop=True)
    #pprint(master_subject_table)
    #pprint(master_subject_table.duplicated())
    return master_subject_table

def create_subject_lookup_table(subject_list):
    lookup_table = pd.DataFrame(subject_list, columns=['subject'])
    lookup_table['transaction'] = np.nan
    lookup_table['submitted'] = np.nan
    return lookup_table

def identify_unique_subjects(subject_list):
    
    # insert the list to the set
    list_set = set(subject_list)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list

def slice_subject_data(data):
    subject_list = []
    for case in data:
        subject_list = subject_list + case['subject_list']
    #pprint(subject_list)
    return subject_list

def pandify_case_data(data):
    #case_df = pd.concat(data, sort=False)
    df= pd.DataFrame(data)
    df['submitted'] = np.nan
    return df
        
def stringify_json_values(data):
    for dict in data:
        subject_list = dict['subject']
        for key in dict:
            if type(dict[key]) == list:
                tmp_list = []
                for item in (dict[key]):
                    item = item.replace(" ", "-")
                    tmp_list.append(item)
                dict[key] = tmp_list

                dict[key] = ",".join(dict[key])
        dict['subject_list'] = subject_list

                
    return data
                

    #pprint(data)

def clean_json_data(filtered_data):
    # Select the keys that I want from the dictionary
    # filter appropriatly into a df 
    # write df to file
    #print(type(filtered_data))
    #pprint(filtered_data)
    for data in filtered_data:
        #pprint(data)
        #creat a dictionary of columns and values for each row.  Combine them all into a df when we are done
        # each dictionary must be a row.... which makes perfect sense, but they can not be nested... 
        item = data.pop('item', None)
        resources = data.pop('resources', None)
        index = data.pop('index', None)
        language = data.pop('language', None)
        online_format= data.pop('online_format', None)
        original_format = data.pop('original_format', None)
        kind = data.pop('type', None)
        image_url = data.pop('image_url', None)
        hassegments = data.pop('hassegments', None)
        extract_timestamp = data.pop('extract_timestamp', None)
        timestampe = data.pop('timestamp', None)
        mimetype=data.pop('mime_type', None)
        try:
            pdf = resources[0]['pdf']
        except: 
            pdf = "noPdf"
        data["pdf"] = pdf
        data['search_index'] = index
    


    # convert to strings maybe move into another function to be called.  Actually will definitely move to a nother function 

    return filtered_data
    #uid = UniqueIdProperty()
    ##date = date
    #dates = dates
    #group = group
    #id = id 
    #pdf = pdf 
    #shelf_id = shelf_id
    #subject = subject
    #primary_topic = primary_topic
    #title = title
    #url = url
    #description = description
    #source_collection = source_collection




def filter_json_data(json_data, filter):
    # Using dict()
    # Extracting specific keys from dictionary

    filter = ['contributor','date', 'dates', 'digitized']
    res = dict((k, json_data[k]) for k in filter if k in json_data)
    return res

def create_master_subject_table():
    table = pd.DataFrame()
    table['subject']= np.nan
    table['transaction']= np.nan
    table['submitted'] = np.nan
    return(table)


def get_citation(data):

    # Remove all occurrence of a characters 's', 'a' & 'i' from the string
    #re.sub(r'(.*)', '', 'foobar (###)')
    #reg = re.compile("(....+)")
    data = data[0]
    title = data['title']
    title = title.split(',')
    citation = title[1]
    citation = citation.replace('.', "")
    citation= re.sub(r'\(.*\)', '', citation )
    citation =citation[:-1]
    print(citation)
    

if __name__ == "__main__":
    neo_applified = instantiate_neo_model_api()
    cwd = get_cwd()
    file_list = get_files(cwd = cwd)

    file = file_list[0]
    data = load_json_data(file=file)
    data = data['results']
    #pprint(data)
    #pprint(data[0])
    
    #filtered_data = filter_json_data(json_data = data, filter = filter)

    # Creating the case nodes transaction nodes and df
    data = clean_json_data(data)
    data = get_citation(data)
    #pprint(data)
    #case_data = stringify_json_values(data)
    #case_data = pandify_case_data(case_data)
    #case_data = nodify_case_data(case_data = case_data)
    
    # Creating the subject nodes transaction nodes and df
    ##subject_list = slice_subject_data(data)
    #subject_list = identify_unique_subjects(subject_list)
    #subject_lookup_table = create_subject_lookup_table(subject_list)
    #master_subject_table = integrate_to_master_table(subject_lookup_table,master_subject_table)
    #pprint(master_subject_table.duplicated())
    #case_counter = case_counter + len(case_data)

    #master_subject_table = nodify_subjects(master_subject_table)

    #master_subject_table = create_master_subject_table()
    #json_pipeline(file_list=file_list, master_subject_table=master_subject_table)
    
    #neo_sandbox_app = instantiate_neo_sandbox_app()
    #google_creds = load_google_creds()
    #sheets_app = instantiate_sheets_app(google_creds.credentials)
    #drive_app = instantiate_drive_app(google_creds.credentials)
    #googleAPI = instantiate_google_API()
    #sparkAPI = instantiate_spark_API()
    #neoAPI = NeoAPI()
    #nodified_df = pandas_functions.nodify_dataframe()
    #test()
    #google_api = googleServices.GoogleAPI()
    ###neo_model_api = instantiate_neo_model_api()
    ###df_pipeline_dictionary = prepare_data_pipeline()
    #final_df_dictionary = upload_data_pipeline_to_neo(df_pipeline_dictionary)
    #for k,v in final_df_dictionary.items():
    #    cwd = os.getcwd()
    #    path = str(k) +"Final"
    #    path = os.sep.join([cwd,path])

     #   with open(path, "w") as file:
     #       v.to_csv(path, index=False)

    #prepared_dfs = prepare_pandas_df()
    #pprint(prepared_df)
    #upload_df_to_db(df = prepared_df, neo_model_api = neo_model_api)

    

    
    




    
    