from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from getpass import getpass

'''
This is a simple of creating a new index, populating it with a list of documents, and running a simple search query
'''

index = "devrel"
documents = [{'Name': 'Iulia',
            'Sentence': 'I like using python',
            'Number': 12345},
            {'Name': 'Carly',
            'Sentence': 'I build search games',
            'Number': 6789}]
settings = {}
mappings = {
        "_meta" : {
            "created_by" : "Iulia Feroli"
        },
        "properties" : {
            "Number" : {
                "type" : "long"
            },
            "Name" : {
                "type" : "keyword",
                "type" : "text"
            },
            "Sentence" : {
                "type" : "text"
            }
        }
    }
query={
        "match": {
            "Sentence": "python"
        }
    }

#Connect to the elastic cloud server
ELASTIC_CLOUD_ID = getpass("Elastic Cloud ID: ")
ELASTIC_USERNAME = getpass("Elastic username: ")
ELASTIC_PASSWORD = getpass("Elastic password: ")

es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID,  # cloud id can be found under deployment management
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD) # your username and password for connecting to elastic, found under Deplouments - Security
)

#Create an index and populate it with the document list
es.indices.create(index=index, settings=settings, mappings=mappings)
bulk(client = es, index = index, actions = iter(documents), stats_only = True )


#Run a simple query
response = es.search(index=index, query=query)

print("We get back {total} results, here are the top ones:".format(total=response["hits"]['total']['value']))
for hit in response["hits"]["hits"]:
    print(hit['_source']['Name'])
    
