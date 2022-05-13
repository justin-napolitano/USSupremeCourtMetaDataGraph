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
#from neoModelAPI import NeoNodes as nn





class PreparePandasDF():
    def __init__(self):
        relationship_list = []
        self.df = self.load_data_to_pandas_df()
        self.nodify_city_column()
        self.nodify_states_column()
        self.nodify_url_column()
        self.nodify_country_column()
        self.unique_state_nodes= self.get_unique_state_nodes()
        self.unique_country_nodes = self.get_unique_country_nodes()
        #pprint(self.unique_state_nodes)
        #pprint(self.df.columns)
        self.unique_state_nodes['state_node'] = self.upload_df(self.unique_state_nodes.state_node)
        self.unique_country_nodes['country_nodes'] =self.upload_df(self.unique_country_nodes.country_node)
        #pprint(self.unique_state_nodes)
        self.df['state_node'] = self.df['state_node'].replace(dict(zip(self.unique_state_nodes.state_name,  self.unique_state_nodes.state_node)))

        
        self.df['country_node'] = self.df['country_node'].replace(dict(zip(self.unique_country_nodes.country_name,  self.unique_country_nodes.country_node)))

        self.unique_state_nodes['country_node'] = self.df['country_node'].replace(dict(zip(self.unique_country_nodes.country_name,  self.unique_country_nodes.country_node)))
        pprint(self.unique_state_nodes["country_node"][0].id)
        #pprint(self.unique_state_nodes.columns)
        #self.set_state_relationships()
        #self.upload_df(self.df.city_node)
        #   pprint(self.df.url_node[0])
        #self.upload_df(self.df.url_node)
        #self.set_url_relationships()

        
        #self.set_url_relationships()

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

        

    def get_unique_state_nodes(self):
        df = self.df.drop_duplicates(subset=['state_name']).copy()
        df.drop(df.columns.difference(['state_node','country_node','state_name','country_name']), 1, inplace=True)
        #pprint(df)

        return df


    def get_unique_country_nodes(self):
        df = self.df.drop_duplicates(subset=['country_name']).copy()
        df.drop(df.columns.difference(['country_node','state_node','country_name', 'state_name']), 1, inplace=True)
        #pprint(df)
        return df

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

    def nodify_country_column(self):
        self.df["country_node"] = neo.neoAPI.create_country_node(code = "USA", name = "United States of America")
        self.df['country_name'] = "USA"
    



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

    prepared_dfs = prepare_pandas_df()
    #pprint(prepared_df)
    #upload_df_to_db(df = prepared_df, neo_model_api = neo_model_api)

    

    
    




    
    