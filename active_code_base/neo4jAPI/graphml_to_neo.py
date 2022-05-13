import glob
from operator import ne
import os
import re
from neo_native_apy import NeoApp
import neoModelAPI

def get_cwd():
    cwd = os.getcwd()
    return cwd



def list_files(cwd ='/', input_directory = 'input'):
    
    path = os.sep.join([cwd,input_directory])
    file_list= [f for f in glob.glob(path + "**/*.graphml", recursive=True)]
  
    return file_list
 
def instantiate_neo_application(uri,user,password):
    application = NeoApp(uri, user, password)
    test_results = application.run_test_query()
    print(test_results)
    return application

def upload_to_neo(neo_application,file_list):
    test = "https://raw.githubusercontent.com/justin-napolitano/supreme-court-neo/main/neo4jAPI/input/test.graphml"
    
    query_call = "call apoc.import.graphml('{}')".format(test) 
    print(query_call)
    response = neo_application.query(query = query_call)
    print(response)





def instantiate_neo_model_api(uri):
    return neoModelAPI.neoAPI(uri)

def main():
    uri = "neo4j+s://7a92f171.databases.neo4j.io"
    #uri = "neo4j+s://b121e108.databases.neo4j.io"
    user = "neo4j"
    password = "RF4Gr2IJTNhHlW6HOrLDqz_I2E2Upyh7o8paTwfnCxg"
    input_directory = 'input'
    cwd = get_cwd()
    file_list = list_files(cwd, input_directory)
    #neo_model_api = instantiate_neo_model_api(uri)
    neo_application=instantiate_neo_application(uri, user, password)
    #print(type(neo_application.driver))
    upload_to_neo(neo_application,file_list)
    #print(file_list)



if __name__ == "__main__":
    main()


#    results, meta = db.cypher_query(query, params)



