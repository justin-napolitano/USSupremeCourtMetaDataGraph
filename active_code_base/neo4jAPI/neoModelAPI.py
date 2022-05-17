from dataclasses import dataclass
from datetime import date
from shelve import Shelf
from neomodel import (config, StructuredNode, StringProperty, IntegerProperty,
    UniqueIdProperty, RelationshipTo, BooleanProperty, EmailProperty, Relationship, DateProperty, db)
from pprint import pprint

class neoAPI():

    def __init__(self,uri,user,psw):
        self.db_init = self.instantiate_neo_model_session(uri,user,psw)    
        
    
    def instantiate_neo_model_session(uri,user,psw):
        
        #config.DATABASE_URL = 'neo4j+s://{}:{}@{}'.format(user, psw, uri)
        config.DATABASE_URL ='bolt://neo4j:beautiful@localhost:7687'
        #config.DATABASE_URL = uri
        return True


    def standard_query():
        results, meta = db.cypher_query(query, params)
        people = [Person.inflate(row[0]) for row in results]

    def create_case_node(date, dates, group,name, pdf, shelf_id, subject, title, url, subject_relationship = True):
        return Case(date=date, dates=dates, group=group,name=name, pdf=pdf, shelf_id=shelf_id, subject=subject, title=title, url=url)


    def create_city_node(name):
        return City(name = name)
        
    def create_country_node(code,name):
        return Country(code = code, name = name)

    def create_state_node(code,name):
        return State(code = code, name = name)

    def create_realtor_search_url_node(url):
        return Realtor_Search_URL(url = url, is_root = True, is_sibling = True, is_parent= False, is_child = False, searched = False)
    
    def create_root_node(url, name = 'realtor.com'):
        return Root(is_root = True,name = name,is_parent =False, is_sibling = False, is_child = False, url = url)
        uid = UniqueIdProperty()

    def create_child_node(url, name = 'realtor.com'):
        return Child(is_root = True,name = name,is_parent =False, is_sibling = False, is_child = False, url = url)

    def create_parent_node(url, name = 'realtor.com'):
        return Parent(is_root = True,name = name,is_parent =False, is_sibling = False, is_child = False, url = url)

    def create_sibling_node(url, name = 'realtor.com'):
        return Sibling(is_root = True,name = name,is_parent =False, is_sibling = False, is_child = False, url = url)
    
    def create_relationship(source,target):
      
        
        rel = source.connect(target)
        return rel

        #print("{}"+".connect" + "{}".format(source,target))
        
    def create_subject_node(name = None,):
        return Subject(name = name)

    def update(obj):
        with db.transaction:
            return obj.save()

class Justice(StructuredNode):
    uuid = UniqueIdProperty()
    justice = StringProperty(unique_index=True, required=True)
    term_start = DateProperty(unique_index=True, required=True)
    term_end = DateProperty(unique_index=True, required=True)
    appointee = StringProperty(unique_index=True, required=True)

class Subject(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)


class Case(StructuredNode):
    uid = UniqueIdProperty()
    date = StringProperty(unique_index=True, required=True)
    dates = StringProperty(unique_index=True, required=True)
    group = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index=True, required=True)
    pdf = StringProperty(unique_index=True, required=True) 
    shelf_id = StringProperty(unique_index=True, required=True)
    subject = StringProperty(unique_index=True, required=True)
    #primary_topic = StringProperty(unique_index=True, required=True)
    title = StringProperty(unique_index=True, required=True)
    url = StringProperty(unique_index=True, required=True)
    subject_relationship = Relationship("Subject", "IS_SUBJECT")

class Processed(StructuredNode):
    uid = UniqueIdProperty()

class NotProcessed(StructuredNode):
    uid = UniqueIdProperty()
    

class City(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    state = Relationship('State', 'IS_STATE_OF')
    country = Relationship('Country', 'IS_COUNTRY_OF')
    
    
class Country(StructuredNode):
    uid = UniqueIdProperty()
    code = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index=True, required=True)
    

class State(StructuredNode):
    uid = UniqueIdProperty()
    code = StringProperty(unique_index=True, required=True)
    name = StringProperty(unique_index=True, required=True)
    country = Relationship('Country', 'IS_COUNTRY_OF')

class Root(StructuredNode):
    uid = UniqueIdProperty()
    is_root = BooleanProperty(unique_index = True, required = True)
    is_parent = BooleanProperty(unique_index = True, required = True)
    is_sibling = BooleanProperty(unique_index = True, required = True)
    is_child = BooleanProperty(unique_index = True, required = True)
    name = StringProperty(unique_index = True, required = False)
    url = StringProperty()
    processed = Relationship("Processed", "IS_PROCESSED")
    NotProcessed = Relationship("NotProcessed", "NOT_PROCESSED")
    sibling = Relationship("Sibling","IS_SIBLING")
    child = Relationship("Child","IS_CHILD")
    parent = Relationship("Parent","IS_PARENT")
    root = Relationship("Root", "IS_ROOT")

class Child(StructuredNode):
    uid = UniqueIdProperty()
    is_root = BooleanProperty(unique_index = True, required = True)
    is_parent = BooleanProperty(unique_index = True, required = True)
    is_sibling = BooleanProperty(unique_index = True, required = True)
    is_child = BooleanProperty(unique_index = True, required = True)
    name = StringProperty()
    processed = Relationship("Processed", "IS_PROCESSED")
    NotProcessed = Relationship("NotProcessed", "NOT_PROCESSED")
    sibling = Relationship("Sibling","IS_SIBLING")
    child = Relationship("Child","IS_CHILD")
    parent = Relationship("Parent","IS_PARENT")
    root = Relationship("Root", "IS_ROOT")

class Parent(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    is_root = BooleanProperty(unique_index = True, required = True)
    is_parent = BooleanProperty(unique_index = True, required = True)
    is_sibling = BooleanProperty(unique_index = True, required = True)
    is_child = BooleanProperty(unique_index = True, required = True)
    processed = Relationship("Processed", "IS_PROCESSED")
    NotProcessed = Relationship("NotProcessed", "NOT_PROCESSED")
    sibling = Relationship("Sibling","IS_SIBLING")
    child = Relationship("Child","IS_CHILD")
    parent = Relationship("Parent","IS_PARENT")
    root = Relationship("Root", "IS_ROOT")


class Sibling(StructuredNode):
    uid = UniqueIdProperty()
    is_root = BooleanProperty(unique_index = True, required = True)
    is_parent = BooleanProperty(unique_index = True, required = True)
    is_sibling = BooleanProperty(unique_index = True, required = True)
    is_child = BooleanProperty(unique_index = True, required = True)
    name = StringProperty()
    processed = Relationship("Processed", "IS_PROCESSED")
    NotProcessed = Relationship("NotProcessed", "NOT_PROCESSED")
    sibling = Relationship("Sibling","IS_SIBLING")
    child = Relationship("Child","IS_CHILD")
    parent = Relationship("Parent","IS_PARENT")
    root = Relationship("Root", "IS_ROOT")
    
class Realtor_com(StructuredNode):
    uid = UniqueIdProperty()
    is_realtor_com = BooleanProperty(unique_index = True, required = True)
    name = StringProperty()

class Realtor_Search_URL(StructuredNode):
    uid = UniqueIdProperty()
    url = StringProperty(unique_index=True, required=True)
    searched = BooleanProperty(unique_index = True, required = True)
    is_root = BooleanProperty(unique_index = True, required = True)
    is_child = BooleanProperty(unique_index = True, required = True)
    is_parent = BooleanProperty(unique_index = True, required = True)
    is_sibling = BooleanProperty(unique_index = True, required = True)
    #state = Relationship('State', 'OF')
    state = Relationship('State', 'IS_STATE_OF')
    city = Relationship('City', 'IS_CITY_OF')
    root = Relationship('Root','IS_ROOT')
    child = Relationship('Child',"IS_CHILD")
    parent = Relationship('Parent', "IS_PARENT")
    sibling = Relationship('Sibling', "IS_SIBLING")
    realtor_com = Relationship('Realtor_com', "IS_REALTOR.COM_URL")
    processed = Relationship("Processed", "IS_PROCESSED")
    NotProcessed = Relationship("NotProcessed", "NOT_PROCESSED")


class Person(StructuredNode):
    uid = UniqueIdProperty()
    full_name = StringProperty(required = True)
    email = EmailProperty()