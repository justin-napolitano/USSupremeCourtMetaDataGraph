from platform import node
from pprint import pprint
#from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
#    UniqueIdProperty, RelationshipTo, BooleanProperty, EmailProperty, Relationship,db)
import pandas as pd
#import NeoNodes as nn
#import GoogleServices
#import sparkAPI as spark
import neoModelAPI as neo
import glob
import os
import json
import numpy as np
import shutil



def instantiate_neo_model_api():
    uri = "7a92f171.databases.neo4j.io"
    user = "neo4j"
    psw = 'RF4Gr2IJTNhHlW6HOrLDqz_I2E2Upyh7o8paTwfnCxg'
    return neo.neoAPI.instantiate_neo_model_session(uri=uri,user=user,psw=psw)

def get_cwd():
    cwd = os.getcwd()
    return cwd


def get_files(cwd =os.getcwd(), input_directory = 'article_data'):
    
    path = os.sep.join([cwd,input_directory])
    #pprint(path)
    file_list= [f for f in glob.glob(path + "**/*.csv", recursive=True)]
  
    return file_list

def get_article_df(file_list = None):
    try:
        for a_file in file_list:
            df = pd.read_csv(a_file )
            return df
    except:
        print('Ah you goofed up')
        raise
       

def get_transaction_df(df = None):  
    #pprint(justice_df)
    try:
        #pprint(df.columns)
        #   df.apply(lambda x: print(x), axis =1)
        df['transaction'] = df.apply(lambda x: neo.neoAPI.create_article_node(name= x['article'],  
        topic = x['topic'], 
        citation = x['citation']),
        axis = 1
        )
        return(df)
    except:
        
        pprint('ahh man you goofed up again')
        raise

def write_transaction_to_file(df, cwd = os.getcwd(),import_directory = 'merge_articles', file_name = 'article_transaction_df'):
    try:
        outfile = os.sep.join([cwd,import_directory,file_name])
        #pprint(outfile)
        df.to_csv(outfile)
        return outfile
    except:
        print('Ahh why you such a goof?')
        raise

def send_closing_message(df = None, outfile= None):
    size = shutil.get_terminal_size((80, 20))
    columns = size[0] -2


    seperator = "*" * columns
    df_message = "Your Final df looks like: "
    outfile_message = "You will find the data at: {}".format(outfile)
    pprint(seperator)
    pprint(df_message)
    pprint(df)
    pprint(seperator)
    pprint(outfile_message)
    return True
    


    


if __name__ == "__main__":
    #neo_applified = instantiate_neo_model_api()
    cwd = get_cwd()
    file_list = get_files(cwd = cwd)
    #pprint(file_list)
    #master_subject_table = create_master_subject_table()
    #json_pipeline(file_list=file_list, master_subject_table=master_subject_table)
    article_df = get_article_df(file_list = file_list)
    article_df = get_transaction_df(df = article_df)
    outfile = write_transaction_to_file(df = article_df , cwd = cwd)
    messaged = send_closing_message(article_df, outfile)


    #pprint(justice_df)