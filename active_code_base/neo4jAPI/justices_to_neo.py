from platform import node
from pprint import pprint
from pty import master_open
from re import sub
from urllib.parse import non_hierarchical
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, BooleanProperty, EmailProperty, Relationship,db)
import pandas as pd
#import NeoNodes as nn
#import GoogleServices
#import sparkAPI as spark
import neoModelAPI as neo
import glob
import os
import json
import numpy as np



def instantiate_neo_model_api():
    uri = "7a92f171.databases.neo4j.io"
    user = "neo4j"
    psw = 'RF4Gr2IJTNhHlW6HOrLDqz_I2E2Upyh7o8paTwfnCxg'
    return neo.neoAPI.instantiate_neo_model_session(uri=uri,user=user,psw=psw)

def get_cwd():
    cwd = os.getcwd()
    return cwd


def get_files(cwd =os.getcwd(), input_directory = 'extras'):
    
    path = os.sep.join([cwd,input_directory])
    file_list= [f for f in glob.glob(path + "**/*.json", recursive=True)]
  
    return file_list

if __name__ == "__main__":
    neo_applified = instantiate_neo_model_api()
    cwd = get_cwd()
    file_list = get_files(cwd = cwd)
    master_subject_table = create_master_subject_table()
    json_pipeline(file_list=file_list, master_subject_table=master_subject_table)