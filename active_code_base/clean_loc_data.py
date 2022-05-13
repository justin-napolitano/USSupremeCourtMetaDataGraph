from distutils.command.clean import clean
import glob
from operator import ne
import os
import re
import json
from pprint import pprint


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def get_cwd():
    cwd = os.getcwd()
    return cwd

def get_files(cwd ='/', input_directory = 'test_output'):
    
    path = os.sep.join([cwd,input_directory])
    file_list= [f for f in glob.glob(path + "**/*.json", recursive=True)]
  
    return file_list

def load_json_data(file):
    f = open (file, "r")
  
    # Reading from file
    data = json.loads(f.read())
    return data

def select_results(json_data):
    ldajkf;akdjf


def dump_json_to_file(json_data = None,file_counter = 0):
    if json_data != None:
        # the json file where the output must be stored
        with cd("cleaned_output"):
            outpath = 'result_{}.json'.format(file_counter)
            out_file = open(outpath, "w")
            json.dump(json_data, out_file, indent = 6)
        
            out_file.close()
        return True

    else: 
        return False

def clean_json(file_list = None):
    if file_list != None:
        file_counter = 0
        for file in file_list:
            data = load_json_data(file=file)
            data = data['results']
            dumped =dump_json_to_file(json_data=data, file_counter=file_counter)
            if dumped == True:
                print("Dumped {} file(s)".format(file_counter +1))
                file_counter = file_counter + 1
            else:
                print("Ahhh man,  thats no good")
                return False
        
        return True
    else:
        return False

    




def main():
    cwd = get_cwd()
    file_list = get_files(cwd = cwd)
    cleaned = clean_json(file_list)
    if cleaned == True:
        print("Everything worked well")
    else:
        print("Everything didn't go well")

if __name__ == "__main__":
    main()
    
