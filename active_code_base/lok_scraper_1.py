#library_of_congress_scraper.py
from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import lxml.etree as etree
import xml.etree.ElementTree as ET
import json
import pandas as pd
import os
import time
import random
import math
from pprint import pprint
#import load_vars as lv
import html
import yaml
from yaml import Loader, Dumper
import glob
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from flatten_json import flatten
import networkx as nx



class node_json():
        def __init__(self, data):
            self.out = self.flatten(data)
            self.graph = nx.Graph()

        def create_node(key):
            testing = "do_something"
            
  
        def node_generator(self, data, name =''):
            output = {}
            keys_at_level = []
            
            # If the Nested key-value 
            # pair is of dict type
            if type(data) is dict:
                for k, v in data:
                    create_node(k)
                    node_generator(v)

            elif type(data) is list:
                for item in data:
                    node_genrator(item)

            else:
                #this item is no longer a dictionary or list
                create_node(data)
  
        #flatten(hierarchak)_dict)
            return out_put

class search_result():
    
    def __init__(self,dict_item,num_columns,colnum_string):
        self.key = dict_item.key()
        self.value = dict_item.value()
        self.column_string = colnum_string
        self.index = num_columns
        self.range = self.create_column_range_string()
        self.request_body = self.create_column_request()

    def create_column_request(self):
        request_body = {
            'range': self.range,
            "majorDimension": "COLUMNS",
            "values": [self.value]
        }
        return request_body

    
    def create_column_range_string(self):

        rnge = "'Sheet1'" + "!" + self.column_string + str(1)
        return rnge
    def colnum_string(self, num_columns):
        string = ""
        while num_columns > 0:
            num_columns, remainder = divmod(num_columns - 1, 26)
            string = chr(65 + remainder) + string
        return string



class google_drive:
    def __init__(self,creds):
        self.service = self.get_drive_service(creds)

    def test(self):
        pprint("hello I exist")

    def get_drive_service(self, creds):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        SCOPES = []
        #creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.

        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

        return service
    
    

    def create_folder(self,title):
        drive_service = self.service
        file_metadata = {
            'name': '{}'.format(title),
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = drive_service.files().create(body=file_metadata,
                                            fields='id').execute()
        print('Folder ID: %s' % file.get('id'))



    def add_spreadsheet_to_folder(self ,folder_id,title):
        drive_service = self.service
    
        file_metadata = {
        'name': '{}'.format(title),
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        }

        res = drive_service.files().create(body=file_metadata).execute()
        #print(res)

        return res

class google_sheet():

    def __init__(self,creds):
        self.service =self.get_sheet_service(creds)


    def get_sheet_service(self,creds):
        service = build('sheets', 'v4', credentials=creds)
        return service.spreadsheets()

class google_creds():

    def __init__(self,creds_path):

        self.creds = self.get_creds(creds_path)
   
    def get_creds(self,creds_path):

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                print("no creds")
            else:
                creds = service_account.Credentials.from_service_account_file(creds_path)
                #creds = ServiceAccountCredentials.from_json_keyfile_name('add_json_file_here.json', SCOPES)
                #flow = InstalledAppFlow.from_client_secrets_file(
                #    'credentials.json', SCOPES)
                #creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            #with open('token.json', 'w') as token:
            #    token.write(creds.to_json())
        return creds

class config():

    def __init__(self,file_path):
        #self.yaml_stream = file("config.yaml", 'r')
        self.data = self.load_config(file_path)


    def load_config(self,file_path):
        #print("test")
        stream = open(file_path, 'r')
        data = yaml.load(stream,Loader = Loader)
        #pprint(data)
        return data

class search_results_page():

    def __init__(self,base_url = "https://www.loc.gov/collections",collection = "united-states-reports",json_parameter = "fo=json",results_per_page = "c=150",query_param = "?",page_param ="sp=",page_num = 1,column_lookup_table = {},num_columns = 0):
        
        self.search_url = self.create_search_url(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)
        self.response = self.request_data()
        self.response_json = self.response_to_json()
        #self.soup_html = self.html_parse()
        self.next_url = self.get_next_url()
        self.page_num = page_num
        self.response_json_flat = self.flatten_result()
        self.num_columns = num_columns
        self.column_lookup_table = column_lookup_table
        self.map_columns_to_lookup_table()



    def create_search_result_node(self):
     
        for item in self.response_json_flat:
            for k,v in item.items():
                if k not in self.column_lookup_table:
                    column_string = self.colnum_string()

                    self.column_lookup_table[k] = self.colnum_string(self.num_columns)
                    self.num_columns += 1
                else:
                    continue

    def append_to_data_list(self,rnge,d,data_list):#rename to _data_list
        request_body_tmp = {
            'range': rnge,
            "majorDimension": "COLUMNS",
            "values": [d]
        }
        data_list.append(request_body_tmp)
    def map_columns_to_batch_request_list(self):
        for item in self.response_json_flat:
            for k,v in item.items():
                mapped_column_key = self.column_lookup_table[k]
                
                rnge = "'Sheet1'" + "!" + column_key + str(1)





    def colnum_string(self):
        string = ""
        while self.num_columns > 0:
            self.num_columns, remainder = divmod(self.num_columns - 1, 26)
            string = chr(65 + remainder) + string
        return string

    def map_columns_to_lookup_table(self):
        for item in self.response_json_flat:
            for k in item.keys():
                if k not in self.column_lookup_table:
                    self.column_lookup_table[k] = self.colnum_string()
                    self.num_columns += 1
                else:
                    continue
        #return column_lookup_table

    def get_next_url(self):
        return (self.response_json['pagination']['next'])


        
    def create_search_url(self,base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num):
        url_sep ="/"
        page_param = page_param +(str(page_num))
        query = "&".join([json_parameter,results_per_page,page_param])
        query = query_param + query
        search_url = url_sep.join([base_url,collection,query])
        #pprint(search_url)
        
        return search_url

    def say_hello(self):
        pprint(self.base_url)

    def request_data(self):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.11 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
                    'Accept-Encoding': 'identity'
                }
        return requests.get(self.search_url,headers=headers)

    def response_to_json(self):
        return self.response.json()

    def html_parse(self):
        soup=BeautifulSoup(self.response.content,'lxml')
        #pprint(soup)
        return soup

    def flatten_result(self):
        flat_result_list = []
        for item in self.response_json['results']:
            flat_json = flatten(item)
            flat_result_list.append(flat_json)
        return flat_result_list


def create_google_credentials_object(creds_path = 'credentials.json'):
    google_credentials_object = google_creds(creds_path)
    return google_credentials_object
    
def create_config_object(file_path = 'config.yaml'):
    config_object = config(file_path)
    return config_object

def search_result_generator(base_url = "https://www.loc.gov/collections",collection = "united-states-reports",json_parameter = "fo=json",results_per_page = "c=150",query_param = "?",page_param ="sp=",page_num = 1,condition =True):

    while condition ==True:
        search_results_page_object = create_search_results_page_object(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)
        if search_results_page_object.next_url != None:
            condition =True
            page_num = page_num + 1
            yield search_results_page_object
        else:
            condition = False
            yield search_results_page_object     
        

def create_search_results_page_object(base_url = "https://www.loc.gov/collections",collection = "united-states-reports",json_parameter = "fo=json",results_per_page = "c=150",query_param = "?",page_param ="sp=",page_num = 1,column_lookup_table = {}):
    #search = search_results(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)
    #pprint(search.search_url)
    return search_results_page(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)

def create_google_drive_object(google_creds):
    drive_service_object = google_drive(google_creds)
    return drive_service_object

def create_google_sheet_object(google_creds):
    sheet_service_object = google_sheet(google_creds)
    return sheet_service_object

def create_new_google_sheet(google_drive_object,folder_id,title):
    sheet_meta_data = google_drive_object.add_spreadsheet_to_folder(folder_id, title)
    return sheet_meta_data

def flatten_result(result_json):
    flat_json = flatten(result_json)
    return flat_json


def main():
    search_result = create_search_results_page_object()
    pprint(search_result.response_json['results'][0])
    
    #flatten_result(search_result.response_json['results'][0])
    #pprint(search_result.response_json['results'][0])
    #config = create_config_object()
    #google_credentials_object = create_google_credentials_object()
    #drive_service_object = create_google_drive_object(google_credentials_object.creds)
    #sheets_service_object = create_google_sheet_object(google_credentials_object.creds)
    #drive_service_object.test()
    #sheet_meta_data = create_new_google_sheet(drive_service_object,config.data['google']['output_folder_id'],'testing')

    #pprint(search_url.base_url)


if __name__ == "__main__":
    main()

        
        

    
