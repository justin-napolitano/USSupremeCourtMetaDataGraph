from ast import In
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
    
    def create_justice_node(justice, term_start,term_end, appointee):
        return Justice(justice = justice, term_start = term_start, term_end = term_end, appointee = appointee)

    def create_article_node(name, topic, citation):
        return Article(name= name, topic = topic, citation = citation)

    def create_section_node(name,topic,citation):
        return Section(name= name, topic = topic, citation = citation)

    def create_clause_node(name, topic, citation):
        return Clause(name=name, topic=topic, citation=citation)

    def create_relationship(source,target):
      
        
        rel = source.connect(target)
        return rel

        #print("{}"+".connect" + "{}".format(source,target))
        
    def create_subject_node(name = None,):
        return Subject(name = name)

    def update(obj):
        with db.transaction:
            return obj.save()

class Subclause(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    topic = StringProperty(unique_index=True, required=True)
    citation = StringProperty(unique_index=True, required=True)
    article = Relationship("Article", "'IS_SUBCLAUSE_OF'")
    clause = Relationship("Article", "'IS_SUBCLAUSE_OF'")
    sibling_clause= Relationship("Clause", "'IS_SUBCLAUSE_OF'")
    case = Relationship("Case", 'IS_SUBCLAUSE_OF')
    #sub_clause = Relationship("Subclause", "IS_SUBCLAUSE_OF")

class Clause(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    topic = StringProperty(unique_index=True, required=True)
    citation = StringProperty(unique_index=True, required=True)
    article = Relationship("Article", "IS_CLAUSE_OF")
    sibling_clause= Relationship("Clause", "IS_CLAUSE_OF")
    sub_clause = Relationship("Subclause", "IS_CLAUSE_OF")
    case = Relationship("Case", 'IS_CLAUSE_OF')

class Section(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    topic = StringProperty(unique_index=True, required=True)
    article = Relationship("Article", "IS_SECTION_OF")
    citation = StringProperty(unique_index=True, required=True)
    clause = Relationship("Clause", "IS_SECTION_OF")
    sub_clause = Relationship("Subclause", "IS_SECTION_OF")
    case = Relationship("Case", 'IS_SECTION_OF')

class Article(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    topic = StringProperty(unique_index=True, required=True)
    citation = StringProperty(unique_index=True, required=True)
    clause = Relationship("Clause", "IS_ARTICLE_OF")
    sub_clause = Relationship("Subclause", "IS_ARTICLE_OF")
    case = Relationship("Case", 'IS_ARTICLE_OF')
    

class Justice(StructuredNode):
    uuid = UniqueIdProperty()
    justice = StringProperty(unique_index=True, required=True)
    term_start = DateProperty(unique_index=True, required=True)
    term_end = DateProperty(unique_index=True, required=True)
    appointee = StringProperty(unique_index=True, required=True)
    case = Relationship("Case", 'IS_JUSTICE_OF')
    opinion = Relationship('Case', 'WROTE_MAJORITY')
    disent = Relationship('Case', 'DISENTED')
    disent_opinion = Relationship('Case', 'WROTE_DISENT')
    



class Subject(StructuredNode):
    uuid = UniqueIdProperty()
    name = StringProperty(unique_index=True, required=True)
    case = Relationship("Case", 'SUBECT_OF')


class Case(StructuredNode):
    #####Media########
    pdf = StringProperty(unique_index=True, required=True) 

    #### Identification Variables####
    uid = UniqueIdProperty()

    group = StringProperty(unique_index=True, required=True)

    loc_title = StringProperty(unique_index=True, required=True)

    url = StringProperty(unique_index=True, required=True)
    
    shelf_id = StringProperty()

    usCite = StringProperty(unique_index=True, required=True)
    
    
    caseId = StringProperty(unique_index=True, required=True)
   
    caseName = StringProperty(unique_index=True, required=True)
    
    scdb_docket_id = StringProperty(unique_index=True, required=True)
    
    scdb_vote_id = StringProperty(unique_index=True, required=True)
    
    scdb_issues_id = StringProperty(unique_index=True, required=True)
    
    supCite = StringProperty(unique_index=True, required=True)
    
    lawEdCite = StringProperty(unique_index=True, required=True)
    
    lexisCite = StringProperty(unique_index=True, required=True)
    
    dockNumb = StringProperty(unique_index=True, required=True)

    ######background Variables########
    name = StringProperty(unique_index=True, required=True)
    petitioner = Relationship('Petitioner', 'IS_PETITIONER')
    petitionState = Relationship('State', 'IS_PETITIONER')

    respondent = Relationship('Respondent', 'IS_RESPONDENT')
    respondentState = Relationship('State', 'IS_RESPONDENT')

    jurisdiction = Relationship('Jurisdiction', 'JURISDICTION')
    
    adminAction = Relationship('Admin', 'ACTION')

    threeJudgeFdc = BooleanProperty()

    origin = Relationship('USCOURT', 'ORIGIN')

    origin_state = Relationship('State', 'ORIGIN')

    source = Relationship('Source', 'SOURCE')

    source_state = Relationship('State', 'SOURCE')

    lc_disagreement = BooleanProperty()

    certReason = Relationship('CertReason', 'REASON')

    lc_disposition = Relationship('Disposition', 'LC_DISPOSITION')

    lc_direction = Relationship('Direction', 'LC_DIRECTION')

    #####3 Chronological #####

    # From Spaethe
    dateArgument = DateProperty()
    dateDecision = DateProperty()
    dateReargue = DateProperty()

    # From LOC
    date = StringProperty(unique_index=True, required=True)
    dates = StringProperty(unique_index=True, required=True)
    
    term = Relationship('Term', 'TERM_OF')
    natCourt = Relationship('Natcourt','NAT_COURT')

    chief = Relationship('Justice', 'IS_CHIEF')

    ######Substantive#####

    subject = StringProperty(unique_index=True, required=True)

    decisionDirection = Relationship('Direction', 'SUP_COURT_MAJORITY_DIRECTION')
    
    decisionDirectionDissent = Relationship('Direction', 'SUP_COURT_DISSENT_DIRECTION')
    
    spaethIssue = Relationship('SpaethIssue', 'IS_SPAETH_ISSUE')
    
    spaethIssueArea = Relationship('SpaethIssueArea', 'IS_SPAETH_ISSUE_AREA')

    subject_relationship = Relationship("Subject", "IS_CASE_OF")
    
    article = Relationship("Case", 'IS_ARTICLE_OF')
    
    clause = Relationship("Clause", 'IS_CLAUSE_OF')
    
    section = Relationship("Section", 'IS_SECTION_OF')
    
    sub_clause = Relationship("Subclause", 'IS_SUB_CLAUSE_OF')
    
    major_case_topic = Relationship('Subject', 'IS_MAJOR_TOPIC')

    authority = Relationship('Authority', 'IS_AUTHORITY')

    legalProvision = Relationship('legalProvision', 'IS_PROVISION')
    
    lawType = Relationship('lawType', 'lawType')

    law = Relationship('Law', 'SUPPORTING_LAW')

   
    ######Outcome Variables#####

    decisionType = Relationship('DecisionType', 'IS_DECISION_TYPE')

    declarationUnconstitutional = Relationship('Constitutional','UNCONSTITUTIONAL')
    
    delcarationConstitutional = Relationship('Constitutional', "CONSTITUTIONAL")

    disposition = Relationship('Disposition', 'IS_DISPOSITION')

    winningParty = Relationship('Party', 'IS_WINNER')
    FormalAlterationOfPrecedent = BooleanProperty()
    
    alteredPrecedent = Relationship("Case", 'Altered_Precedent')
    

    ## Voting and Opinion Variables
    # will account for all types of votes a node for each outcome
    vote = Relationship('Vote', 'OUTCOME')
    
    majOpinWriter = Relationship('Justice', 'WROTE_MAJORITY_OPINION')
    
    majOpinWriter = Relationship('Justice', "ASSIGNED_MAJORITY_OPINION")

    affirmative_vote = Relationship('Justice', "AFFIRMATE_VOTE")
    
    negative_vote = Relationship('Justice', "NEGATIVE_VOTE")

    conservative_vote = Relationship('Justice', 'CONSERVATIVE')
    liberal_vote = Relationship('Justice', "LIBERAL")

    majority_vote = Relationship('Justice', 'MAJORITY_VOTE')

    miniority_vote = Relationship('Justice','MINORITY_VOTE')

    wrote_an_opinion = Relationship('Justice', 'WROTE_AN_OPINION')

    co_authored_opinion = Relationship('Justice', "COAUTHORED_OPINION")

    agreed_with_concurrence = Relationship('Justice', 'AGREED_WITH_CONCURRENCE')

    agreed_with_dissent = Relationship('Justice', 'AGREED_WITH_CONCURRENCE')


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