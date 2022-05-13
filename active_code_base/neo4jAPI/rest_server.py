from neo4j import GraphDatabase,basic_auth
from neo4j.expections import ServiceUnavailable
import neo_native_app as neo4j
import json
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, Docker!'


@app.route('/init_neo_driver')
def db_init():
    bolt ="bolt://127.0.0.0:7687"
    password = "5995Oscar"
    user = "neo4j"
    driver = neo4j.NeoSandboxApp(bolt,user,password)
    number_nodes = driver.run_test_query()
    response = {"number_nodes": number_nodes}
    return json.dumps(response)


if __name__ == "__main__":
  app.run(host ='0.0.0.0')
