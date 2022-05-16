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
import mimetypes
from platform import node
from pprint import pprint
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
#from neoModelAPI import NeoNodes as nn


class DataUploadFunctions():
    def upload_df(self,df):
        #df.apply(lambda x: pprint(str(x) + str(type(x))))
        
        node_list =  df.apply(lambda x: neo.neoAPI.update(x))
        #pprint(node_list)
        return  node_list
    
    def map_to_df(self,df1,df2,lookup_value :str, lookup_key: str):
        df1[lookup_value] = df1[lookup_key]
        #pprint(df1.columns)
        #pprint(df1)
        
        val  = df1[lookup_value].replace(dict(zip(df2[lookup_key],  df2[lookup_value])))
        return val

    def set_relationships(self,source_node, target_node):
        #pprint(self.df.columns)
        #pprint(source_node)
        rel = neo.neoAPI.create_relationship(source = source_node ,target = target_node)
        return rel

class DataPipelineFunctions():
    def write_df_to_csv(self,df,path: str):
        cwd = os.getcwd()
        path = os.sep.join([cwd,path])

        with open(path,'w') as f:
            df.to_csv(path, index=False)

        return path

    def create_city_nodes(self,df):
        city_nodes = df['city_name'].apply(lambda x :neo.neoAPI.create_city_node(name = x))
        return city_nodes

    def create_url_nodes(self,df):
        url_nodes = df['root_realtor_url'].apply(lambda x :neo.neoAPI.create_realtor_search_url_node(url= x))
        return url_nodes
    
    def create_root_nodes(self,df):
        root_nodes = df['root_realtor_url'].apply(lambda x :neo.neoAPI.create_root_node(url= x))
        return root_nodes

    def create_country_nodes(self,df):
        country_nodes = df.apply(lambda x :neo.neoAPI.create_country_node(code = x.country_code, name = x.country_name),axis =1)
        return country_nodes
        

    def return_unique_country_df(self,df):
        df = df.drop_duplicates(subset=['country_name']).copy()
        df.drop(df.columns.difference(['country_node','state_node','country_name', 'country_code','state_name']), 1, inplace=True)
        #pprint(df)
        return df


    def create_state_nodes(self,df):
        state_nodes = df.apply(lambda x :neo.neoAPI.create_state_node(code = x.state_code, name = x.state_name),axis =1)
        return state_nodes    

    def return_unique_state_df(self,df):
        df = df.drop_duplicates(subset=['state_name']).copy()
        df.drop(df.columns.difference(['state_node','country_node','country_code','state_name','country_name','state_code']), 1, inplace=True)
        #pprint(df)

        return df

    def rename_columns(self,df, mapper = {'city': 'city_name', 'state': 'state_code','realtor_url': 'root_realtor_url'}):
        return df.rename(columns = mapper)


    def add_country_code(self,country_code = "USA"):
        return country_code

    def add_country_name(self,country_name = "United States of America"):
        return country_name

    def upload_df(self,df):
        #df.apply(lambda x: pprint(str(x) + str(type(x))))
        
        node_list =  df.apply(lambda x: neo.neoAPI.update(x))
        pprint(node_list)
        return  node_list
        #df['server_node'] =  node_list
        #pprint(df)
        
        


    def set_url_relationships(self):
        #pprint(self.df.columns)
        update_list = self.df.apply(lambda x: neo.neoAPI.create_relationship(source = x.url_node.city,target = x.city_node), axis=1)
        pprint(update_list)
        return update_list
        #rel = self.df.url.connect(self.df.city)

    def set_city_relationships(self):
        #pprint(self.df.columns)
        update_list = self.df.apply(lambda x: neo.neoAPI.create_relationship(source = x.city_node.country,target = x.country_node), axis=1)
        update_list = self.df.apply(lambda x: neo.neoAPI.create_relationship(source = x.city_node.state,target = x.state_node), axis=1)
        pprint(update_list)
        #rel = self.df.url.connect(self.df.city)

    def set_state_relationships(self):
        #pprint(self.df.columns)
        neo.neoAPI.create_relationship(source = self.unique_state_nodes.state_node[0].country,target = self.unique_state_nodes.country_node[0])
        #update_list = self.unique_state_nodes.apply(lambda x: neo.neoAPI.create_relationship(source = x.state_node.country,target = x.country_node.name), axis=1)
        #pprint(update_list)
        #rel = self.df.url.connect(self.df.city)




    def group_by_state(self):
        grouped = self.df.groupby(by = "state_name")
        
    def load_data_to_pandas_df(self,file_path = None):
        if file_path != None:

            with open (file_path) as file:
                df = pd.read_json(file)
            return df
    
    def nodify_city_column(self):
        self.df['city_node'] = self.df['city'].apply(lambda x : neo.neoAPI.create_city_node(name = x))
        
        
        #pprint(df.city_nodes)



    def nodify_states_column(self):

        unique_states = self.df.drop_duplicates(subset=['state']).copy()
        #pprint(state_dict)

        unique_states['state_node'] = unique_states.apply(lambda x: neo.neoAPI.create_state_node(name = x.state_name, code = x.state), axis=1)
        #pprint(unique_states)
        #self.df['state_nodes'] = unique_states['state_nodes'] where unique_states[state_name] = self.df_stateName
        self.df["state_node"] = self.df['state_name']
        #self.df['state_node'] =
        #pprint(self.df['state_name'].map(unique_states))
        self.df['state_node'] = self.df['state_node'].replace(dict(zip(unique_states.state_name,  unique_states.state_node)))
        #pprint(self.df)

        
     
        #mask = dfd['a'].str.startswith('o')
        
        
        #self.df['state_nodes'] = self.df.apply(lambda x: neo.create_state_node(name = x.state_name, code = x.state) if x not in states_dict else states_dict[x], axis=1)
        
    def nodify_url_column(self):
        self.df['url_node'] = self.df['realtor_url'].apply(lambda x : neo.neoAPI.create_url_node(url = x, searched= False))


    

def get_cwd():
    cwd = os.getcwd()
    return cwd

def get_files(cwd =os.getcwd(), input_directory = 'input'):
    
    path = os.sep.join([cwd,input_directory])
    file_list= [f for f in glob.glob(path + "**/*.json", recursive=True)]
  
    return file_list

def instantiate_neo_model_api():
    uri = "7a92f171.databases.neo4j.io"
    user = "neo4j"
    psw = 'RF4Gr2IJTNhHlW6HOrLDqz_I2E2Upyh7o8paTwfnCxg'
    return neo.neoAPI.instantiate_neo_model_session(uri=uri,user=user,psw=psw)

def prepare_data_pipeline():
    pipeline_functions = DataPipelineFunctions()
    master_df = pipeline_functions.load_data_to_pandas_df()
    master_df['country_name'] = pipeline_functions.add_country_name()
    master_df['country_code'] = pipeline_functions.add_country_code()
    master_df = pipeline_functions.rename_columns(master_df)
    master_df['city_node'] = pipeline_functions.create_city_nodes(master_df)
    master_df['url_node'] = pipeline_functions.create_url_nodes(master_df)
    master_df['root_node'] = pipeline_functions.create_root_nodes(master_df)

    
    master_df_path = pipeline_functions.write_df_to_csv(master_df,'master_df.csv')

    

    
    state_df = pipeline_functions.return_unique_state_df(master_df)
    state_df['state_node'] = pipeline_functions.create_state_nodes(state_df)
    state_df_path = pipeline_functions.write_df_to_csv(state_df,'state_df.csv')
    

    country_df = pipeline_functions.return_unique_country_df(master_df)
    country_df['country_node'] = pipeline_functions.create_country_nodes(country_df)
    country_df_path = pipeline_functions.write_df_to_csv(country_df,'country.csv')


    



    #upload nodes
    
    return {"master_df" : master_df, 'state_df' : state_df, 'country_df': country_df}



def load_json_data(file):
    f = open (file, "r")
  
    # Reading from file
    data = json.loads(f.read())
    return data


def json_pipeline(file_list, master_subject_table):
    test = file_list[0]
    data = load_json_data(file=test)
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
    master_subject_table = nodify_subjects(master_subject_table)

    #lets save data to the database

    master_subject_table = submit_subjects_to_db(master_subject_table)
    case_data = submit_cases_to_db(case_data = case_data)

    # Create Relationships

    relationship_list= create_relationship_table(case_data=case_data, master_subject_table=master_subject_table)
    




def submit_cases_to_db(case_data):
        #unsubmitted = master_subject_table[master_subject_table.notna()]
    non_submitted_nodes = case_data[case_data.isna().any(axis=1)]
    #pprint(non_submitted_nodes)
    non_submitted_nodes['submitted'] = non_submitted_nodes['transaction'].apply(lambda x: neo.neoAPI.update(x))
    #test = non_submitted_nodes.iloc[32]['transaction']
    #return_obj = neo.neoAPI.update(test)
    case_data.update(non_submitted_nodes)
    return case_data

    #Relationships must need to be created following saving to the df
    #relationships = create_relationship_table(case_data, master_subject_table)

def submit_subjects_to_db(master_subject_table):
    #unsubmitted = master_subject_table[master_subject_table.notna()]
    non_submitted_nodes = master_subject_table[master_subject_table.isna().any(axis=1)]
    #pprint(non_submitted_nodes)
    non_submitted_nodes['submitted'] = non_submitted_nodes['transaction'].apply(lambda x: neo.neoAPI.update(x))
    #test = non_submitted_nodes.iloc[32]['transaction']
    #return_obj = neo.neoAPI.update(test)
    master_subject_table.update(non_submitted_nodes)
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
        for subject_row in range(len(unique_dataframe)):
            case = case_data.iloc[row]['submitted']
            subject = unique_dataframe.iloc[subject_row]['submitted']
            #create relationship
            relationship = neo.neoAPI.create_relationship(case.subject_relationship,subject)
            pprint(relationship)
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
    pprint(non_submitted_nodes)
    case_nodes = non_submitted_nodes.apply(lambda x :neo.neoAPI.create_case_node(date = x['date'], dates= x['dates'],group = x['group'], name=x['id'], pdf= x['pdf'], shelf_id = x['shelf_id'], subject= x['subject'], primary_topic = x['subject_major_case_topic'], title = x['title'], url = x['url'], subject_relationship=True), axis=1)

    case_data['transaction'] = case_nodes
    return case_data




def filter_case_data(data):
    pprint(data[0])



def nodify_subjects(master_subject_table):
    non_submitted_nodes = master_subject_table[master_subject_table.isna().any(axis=1)]
    #df[df.isna().any(axis=1)]
    #pprint(non_submitted_nodes)
    subject_nodes = non_submitted_nodes['subject'].apply(lambda x :neo.neoAPI.create_subject_node(name = x))
    master_subject_table['transaction'] = subject_nodes
    return master_subject_table

def integrate_to_master_table(subject_lookup_table, master_subject_table):
    #check_if subject in list is in subject of the table
    # if so drop it from the temp table
    # append what is left to the master table 
    #pprint(subject_lookup_table)
    test = master_subject_table['subject']
    unique_dataframe = (subject_lookup_table[~subject_lookup_table['subject'].isin(test)])
    #duplicate_list = (master_subject_table[~master_subject_table['subject'].isin(subject_lookup_table['subject'])])
    master_subject_table = pd.concat([master_subject_table,unique_dataframe])
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
#def combine_subjects(subject_lists):





    #for each result in the list
        #nodify it 
        # how
            # idk what is necessary for a node
            #Create a node with the properties.  So what is the code
            # i might just have to code hte variables  Otherwise i could unwind it, but then... what 
            #yeah there is a query function
            #nah do it the right way.  
            #FOr each result create a node typed correctly
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
    for data in filtered_data:
        #creat a dictionary of columns and values for each row.  Combine them all into a df when we are done
        # each dictionary must be a row.... which makes perfect sense, but they can not be nested... 
        item = data.pop('item', None)
        resources = data.pop('resources', None)
        index = data.pop('index', None)
        language = data.pop('language', None)
        online_format= data.pop('online_format', None)
        original_format = data.pop('original_format', None)
        type = data.pop('type', None)
        image_url = data.pop('image_url', None)
        hassegments = data.pop('hassegments', None)
        extract_timestamp = data.pop('extract_timestamp', None)
        timestampe = data.pop('timestamp', None)
        mimetype=data.pop('mime_type', None)
        pdf = resources[0]['pdf']
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

if __name__ == "__main__":
    neo_applified = instantiate_neo_model_api()
    cwd = get_cwd()
    file_list = get_files(cwd = cwd)
    master_subject_table = create_master_subject_table()
    json_pipeline(file_list=file_list, master_subject_table=master_subject_table)
    
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

    

    
    




    
    