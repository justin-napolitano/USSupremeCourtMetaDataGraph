from neo4j import GraphDatabase,basic_auth
import logging
from neo4j.exceptions import ServiceUnavailable

class NeoAuraAPI():


    def __init__(self):
        self.aura_driver = self.instantiate_neo_Aura_app()
        #self.run_test_query()

    def instantiate_neo_aura_app(self):
        neo_uri = "neo4j+s://b121e108.databases.neo4j.io"
        neo_user = "<neo4j>"
        neo_password = "<STbDZyKf5_5Nd26AkXcpI__XnGX2VjKfbVY_rPO3uYI>"

        driver = GraphDatabase.driver(neo_uri, auth=(neo_user, neo_password))
        return driver

    def close(self):
        self.driver.close()


class NeoSandboxAPI():


    def __init__(self):
        self.sanbox_driver = self.instantiate_neo_sandbox_app()
        self.run_test_query()

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
            for record in results:
                print(record['count'])


    def instantiate_neo_sandbox_app(self):
        bolt = "bolt://54.147.65.170:7687"
        user = "neo4j"
        password = "pulses-blank-dittos"
        sandbox_driver = GraphDatabase.driver(bolt,auth=basic_auth(user, password))
        
        return sandbox_driver

    def close(self):
        self.driver.close()