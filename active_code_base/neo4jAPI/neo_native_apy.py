from neo4j import GraphDatabase,basic_auth
import logging
from neo4j.exceptions import ServiceUnavailable
import json


class NeoSandboxApp():
    def __init__(self, bolt, user, password):
        self.driver = GraphDatabase.driver(
        bolt,
        auth=basic_auth(user, password))

    def run_test_query(self):
        limit = 10
        cypher_query = f'''
        MATCH (n)
        RETURN COUNT(n) AS count
        LIMIT {limit}
        '''


        with self.driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx: tx.run(cypher_query).data())
            #for record in results:
            #    print(record['count'])
            results = [x['count'] for x in results]
        return results


    def set_property_by_id(self, id_label_obj,property,value):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._set_property_by_id, id_label_obj, property, value)
            return result
            

    @staticmethod
    def _set_property_by_id(tx, id_label_obj, property,value):

        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        match_statement = (f"MATCH (n:{id_label_obj.label}) where (id(n) = {id_label_obj.id} )")
        set_statement = (f"SET n.{property} =  {value}")
        query = " ".join([match_statement,set_statement])
        try:
            #print(query)
            result = tx.run(query) 
            result = [record for record in result]
            return result
        # Capture any errors along with the query and data for traceabilityx    
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_relationship_by_id(self, id_label_obj_1,id_label_obj_2, relationship_struct,relationship_type):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_relationship_by_id, id_label_obj_1, id_label_obj_2,relationship_struct,relationship_type)
            return result
            

    @staticmethod
    def _create_relationship_by_id(tx, id_label_obj_1, id_label_obj_2, relationship_struct,relationship_type):

        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        match_and_return = (f"MATCH (n1:{id_label_obj_1.label}) where id(n1) = {id_label_obj_1.id} MATCH (n2:{id_label_obj_2.label}) where id(n2) = {id_label_obj_2.id}")
        query = (f"{match_and_return} CREATE (n1)-[ {relationship_struct} ]->(n2) return {relationship_type}")
        #query_2 = ("MATCH (n1:$id_label_obj_1.label) where id(n1) = $id_label_obj_1.id MATCH (n2:$id_label_obj_2.label) where id(n2) = $id_label_obj_2.id RETURN n1,n2 CREATE (n1)-[$relationship_struct]->(n2))")
        #print(relationship_part)
        #query = (f"MATCH (n1{node_1_struct}) Match (n2{node_2_struct}) return n1,n2")
        #print(query_2)
        try:
            #result = tx.run("MATCH (n1: $label_1 ) where id(n1) = $id_1 .id MATCH (n2: $label_2 ) where id(n2) = $id_2 RETURN n1,n2 CREATE (n1)-[ $relationship_struct ]->(n2))",label_1 = id_label_obj_1.label,id_1= id_label_obj_1.id, label_2 = id_label_obj_2.label, id_2 = id_label_obj_2.id,relationship_struct= relationship_struct)
            result = tx.run(query) 
            result = [record for record in result]
            return result
        # Capture any errors along with the query and data for traceabilityx    
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


    def return_root_url(self, search_string):

        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            print("start")
            result = session.write_transaction(self._match_and_return_search_url, search_string)
        return result

    @staticmethod
    def _match_and_return_search_url(tx,search_url):
        query = search_url
        #print(query)
        result = tx.run(query)
        result = [record for record in result]
        return result


    def create_relationship(self, node_1,node_2, relationship_struct):

        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            print("start")
            result = session.write_transaction(self._create_relationship, node_1, node_2, relationship_struct)
        return result

    @staticmethod
    def _create_relationship(tx,node_1,node_2, relationship_struct):
        query = (
            f"CREATE ({node_struct})\
            return apoc.convert.toJson({node_label}) as output"
            )
        #print(query)
        result = tx.run(query)
        result = [record for record in result]
        return result

    def add_node(self,node_struct,node_label):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            print("start")
            result = session.write_transaction(self._add_node, node_struct,node_label)
        return result

    @staticmethod    
    def _add_node(tx,node_struct,node_label):
        query = (
            f"CREATE ({node_struct})\
            return apoc.convert.toJson({node_label}) as output"
            )
        #print(query)
        try:
            result = tx.run(query)
            result = [record for record in result]
            return result
        except:
            return False

    def return_to_process_stack_node(self, node_property_struct, limit = 1):
        common_label = node_property_struct.common_label
        node_label = node_property_struct.label
        node_property_struct = node_property_struct.struct
        limit = limit

        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
                print("start")
                result = session.read_transaction(self._match_and_return_node, node_property_struct,common_label,limit)
                #print(result)
            #print(result)
        return result 
    
    @staticmethod
    def _match_and_return_node(tx,node_property_struct, common_label, limit):
        query = (
             f"MATCH ({node_property_struct}) with apoc.convert.toJson({common_label}) as output RETURN output limit {limit}"
        )
        #print(query)
        result = tx.run(query)
        print(result)
        

        result = [record for record in result]
        #result = json.dumps(result)

        try:
            return(result)
            
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


    def return_node_related_to_node(self,node_1,relation_to,node_2 ,limit):

            with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
                print("start")
                result = session.read_transaction(self._match_and_return_related_node, node_1, relation_to, node_2, limit)
                #print(result)
            #print(result)
            return result 
    
    @staticmethod
    def _match_and_return_related_node(tx,node_1,relation_to,node_2,limit):
        query = (
             f"MATCH (n: {node_1})-[r: {relation_to} ]->(search_node: {node_2}) with apoc.convert.toJson(search_node) as output RETURN output limit {limit}"
        )
        #print(query)
        result = tx.run(query)
        print(result)
        

        result = [record for record in result]
        #result = json.dumps(result)

        try:
            return(result)
            
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


    def create_friendship(self, person1_name, person2_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name)
            for row in result:
                print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]

        
    def close(self):
        self.driver.close()


class NeoApp:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def run_test_query(self):
        print("testing")
        limit = 10
        cypher_query = f'''
        MATCH (n)
        RETURN COUNT(n) AS count
        LIMIT {limit}
        '''


        with self.driver.session(database="neo4j") as session:
            results = session.read_transaction(
                lambda tx: tx.run(cypher_query).data())
            #for record in results:
            #    print(record['count'])
            results = [x['count'] for x in results]
        return results
        

    def create_friendship(self, person1_name, person2_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name)
            for row in result:
                print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]


    def query(self, query, parameters=None, db=None):
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.driver.session(database=db) if db is not None else self.driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response


if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    uri = "neo4j+s://7a92f171.databases.neo4j.io"
    #uri = "neo4j+s://b121e108.databases.neo4j.io"
    user = "neo4j"
    password = "RF4Gr2IJTNhHlW6HOrLDqz_I2E2Upyh7o8paTwfnCxg"
    neo_app = NeoApp(uri, user, password)
    #app.create_friendship("Alice", "David")
    #app.find_person("Alice")
    neo_app.close()
    print("all good!")