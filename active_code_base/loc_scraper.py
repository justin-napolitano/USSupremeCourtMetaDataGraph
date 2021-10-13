#library_of_congress_scraper.py
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

class search_collections():

    def __init__(self,base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num):
        
        self.search_url = self.create_search_url(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)
        self.response = self.request_data()
        self.response_json = self.response_to_json()
        #self.soup_html = self.html_parse()
        self.next_url = self.get_next_url()
        #pprint(self.next_url)
    

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
    


        


def create_search_collection_object(base_url = "https://www.loc.gov/collections",collection = "united-states-reports",json_parameter = "fo=json",results_per_page = "c=150",query_param = "?",page_param ="sp=",page_num = 240,nxt =True):
    #search = search_collections(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)
    #pprint(search.search_url)

    
    while nxt == True:
        search = search_collections(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)
        if search.next_url != None:
            nxt =True
            page_num = page_num + 1
            yield search
        else:
            nxt = False
            yield search


    #if search.next_url != None:
    #    create_search_collection_object(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num+1)
    #    
    #else:
    #    pprint("no_more_to_search")
    #return 1
        #yield search

    #page_num = page_num +1
    #test if good
    #for search in create_search_collection_object(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num+1):
    #    search = create_search_collection_object(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num)
     #   if search.next_url != None:
     #       yield(search)
     #       pprint(search.next_url)
     #   else:
     #       yield(search)
     #       pprint(search.next_url)
            #create_search_collection_object(base_url,collection,json_parameter,results_per_page,query_param,page_param,page_num+1)
        #pprint(search.next_url)
        


#logic
    #Create an object
    #parse it for the necessary data
    #upload data to a sheet
    
#def get_search_collection_response():
#    return search_collections()

def main():
    for x in create_search_collection_object():
        pprint(x.next_url)
    #pprint(search.search_url)
    #pprint(search_url.base_url)


if __name__ == "__main__":
    main()

        
        

    
