#loc_scraper_test.py
import pytest
from pprint import pprint
from active_code_base.lok_scraper_1 import create_search_result_object
from active_code_base.lok_scraper_1 import search_result_generator
from active_code_base.lok_scraper_1 import load_config_file
from active_code_base.lok_scraper_1 import create_google_credentials_object
import yaml
from yaml import Loader, Dumper
#from active_code_base.loc_scraper import get_search_collection_response


def test_create_google_credentials_object():
    file_path = '/Users/justinnapolitano/Dropbox/python/Projects/webscraping/supreme_court_cases/active_code_base/credentials.json'
    google_credentials_object = create_google_credentials_object(creds_path=file_path)
    assert google_credentials_object != None

def test_load_config_file():

    file_path = '/Users/justinnapolitano/Dropbox/python/Projects/webscraping/supreme_court_cases/active_code_base/config.yaml'
    stream = open(file_path, 'r')
    test_data = yaml.load(stream,Loader = Loader)
 
    config_object = load_config_file(file_path)
    #pprint(config_object.data)

    assert config_object.data == test_data 


def test_create_search_collection_object():
    #for item in yielded by generator:
    #    Check the below
    search_result_object = create_search_result_object()
    #search_collection_obj = create_search_collection_object()
    #test if object is created assert that object is not none
    assert search_result_object != None
    assert search_result_object.search_url == 'https://www.loc.gov/collections/united-states-reports/?fo=json&c=150&sp=1'
    assert search_result_object.response != None
    assert search_result_object.response_json != None
        #assert search_collection_obj.soup_html !=None

def test_search_result_generator():
    for search_result_object in search_result_generator(page_num = 244):
        expected_url = 'https://www.loc.gov/collections/united-states-reports/?fo=json&c=150&sp={page_num}'
        expected_url = expected_url.format(page_num = search_result_object.page_num)
        assert search_result_object != None
        assert search_result_object.search_url == expected_url
        assert search_result_object.response != None
        assert search_result_object.response_json != None




    #assert collection_search_url.search_url == "https://www.loc.gov/collections/united-states-reports/?fo=json&at=results"


#def test_get_search_collection_response():



