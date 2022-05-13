#realtor_graph.py


#from neo4j_connect_2 import NeoSandboxApp
#import neo4j_connect_2 as neo
import GoogleServices as google
from pyspark.sql import SparkSession
from pyspark.sql.functions import struct
from pprint import pprint
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, BooleanProperty, EmailProperty, Relationship,db)
import pandas as pd
#import NeoNodes as nn
import GoogleServices
import neo4jClasses
import sparkAPI as spark
import neoModelAPI as neo
import os
#from neoModelAPI import NeoNodes as nn



def upload_data_pipeline_to_neo(df_pipeline_dictionary):
    upload = DataUploadFunctions()
    df_pipeline_dictionary['country_df']['country_node'] = upload.upload_df(df_pipeline_dictionary['country_df']['country_node'])
    df_pipeline_dictionary['state_df']['country_node'] = upload.map_to_df(df1 = df_pipeline_dictionary['state_df'],df2 = df_pipeline_dictionary['country_df'],lookup_key='country_code',lookup_value='country_node')
    df_pipeline_dictionary['master_df']['country_node'] = upload.map_to_df(df1 = df_pipeline_dictionary['master_df'],df2 = df_pipeline_dictionary['country_df'],lookup_key='country_code',lookup_value='country_node')

    df_pipeline_dictionary['state_df']['state_node'] = upload.upload_df(df_pipeline_dictionary['state_df']['state_node'])
    df_pipeline_dictionary['master_df']['state_node'] = upload.map_to_df(df1 = df_pipeline_dictionary['master_df'],df2 = df_pipeline_dictionary['state_df'],lookup_key='state_code',lookup_value='state_node')
   
    #pprint(df_pipeline_dictionary['master_df'].columns)

    #pprint(df_pipeline_dictionary['state_df'])
    #df_pipeline_dictionary['state_df']['related'] = df_pipeline_dictionary['state_df'].apply(lambda x : pprint(x.state_node), axis = 1)
    df_pipeline_dictionary['state_df']['state_to_country'] = df_pipeline_dictionary['state_df'].apply(lambda x : upload.set_relationships(x.state_node.country , x.country_node), axis = 1)


    df_pipeline_dictionary['master_df']['city_node'] = upload.upload_df(df_pipeline_dictionary['master_df']['city_node'])
    df_pipeline_dictionary['master_df']['city_to_state'] = df_pipeline_dictionary['master_df'].apply(lambda x : upload.set_relationships(x.city_node.state , x.state_node), axis = 1)

    df_pipeline_dictionary['master_df']['url_node'] = upload.upload_df(df_pipeline_dictionary['master_df']['url_node'])
    df_pipeline_dictionary['master_df']['url_node_to_state'] = df_pipeline_dictionary['master_df'].apply(lambda x : upload.set_relationships(x.url_node.state , x.state_node), axis = 1)


    df_pipeline_dictionary['master_df']['root_node'] = upload.upload_df(df_pipeline_dictionary['master_df']['root_node'])
    df_pipeline_dictionary['master_df']['url_node_to_root_node'] = df_pipeline_dictionary['master_df'].apply(lambda x : upload.set_relationships(x.url_node.root , x.root_node), axis = 1)


    

    return df_pipeline_dictionary








    
    
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
        
    def load_data_to_pandas_df(self,file_path = "/Users/justinnapolitano/Dropbox/python/Projects/webscraping/realtorGraph/uscities.csv"):
        with open (file_path) as file:
            df = pd.read_csv(file)
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


    



def instantiate_google_API():
    print("Instantiating all google apis")
    google_apis = GoogleServices.GoogleAPI()
    return google_apis 

def instantiate_spark_API():
    print("Instantiating the Spark API")
    sparkAPI = spark.SparkAPI()
    return sparkAPI 

def prepare_pandas_df():
    prepared_df_obj = PreparePandasDF()
    return prepared_df_obj.df

def instantiate_neo_model_api():
    return neo.neoAPI()
    

def upload_df_to_db(df, neo_model_api):
    #neo_model_api.update(df['city_nodes'][2])
    df.unique_state_nodes.apply(lambda x: neo_model_api.update(x))
    df.unique_country_nodes.apply(lambda x: neo_model_api.update(x))
    df.url_nodes.apply(lambda x: neo_model_api.update(x))
    df.city_nodes.apply(lambda x: neo_model_api.update(x))
    

def load_data_to_spark_df(sparkAPI):
    file_path = "/Users/justinnapolitano/Dropbox/python/Projects/webscraping/realtorGraph/uscities.csv"
    df = sparkAPI.load_spark_data_from_csv(file_path)
    df.show(2,truncate=False) 
    return df

def prepare_df_for_upload(df):
    df2 = df.withColumn('state_node', struct(df.state_name.alias("state_name"),df.state.alias("state_code")))
    #rdd2 = df.rdd.map(lambda x: func1(x))
    
    df3=rdd2.toDF(['city','state', 'state_name', 'realtor_url', 'searched','state_node'])

    #df 2 = df.withColumn("state_nodedf.select(struct('age', 'name').alias("struct")).collect()
    #NeoNodes.StateNode(df.state_name, df.state))
    df2.show(4,truncate=False) 
    #df3.show(4,truncate=False) 



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


if __name__ == "__main__":
    #neo_app= instantiate_neo_aura_app()
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
    neo_model_api = instantiate_neo_model_api()
    df_pipeline_dictionary = prepare_data_pipeline()
    final_df_dictionary = upload_data_pipeline_to_neo(df_pipeline_dictionary)
    #for k,v in final_df_dictionary.items():
    #    cwd = os.getcwd()
    #    path = str(k) +"Final"
    #    path = os.sep.join([cwd,path])

     #   with open(path, "w") as file:
     #       v.to_csv(path, index=False)

    #prepared_dfs = prepare_pandas_df()
    #pprint(prepared_df)
    #upload_df_to_db(df = prepared_df, neo_model_api = neo_model_api)

    

    
    




    
    