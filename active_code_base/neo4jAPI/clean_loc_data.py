import glob
from operator import ne
import os
import re

def get_files(cwd ='/', input_directory = 'test_output'):
    
    path = os.sep.join([cwd,input_directory])
    file_list= [f for f in glob.glob(path + "**/*.json", recursive=True)]
  
    return file_list


def main():
    file_list = get_files()

if __name__ == "__main__":
    main()
    
