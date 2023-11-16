from elasticsearch import Elasticsearch
from elasticsearch.client import MlClient
from getpass import getpass

index = "devrel"

#Connect to the elastic cloud server
ELASTIC_CLOUD_ID = getpass("Elastic Cloud ID: ")
ELASTIC_USERNAME = getpass("Elastic username: ")
ELASTIC_PASSWORD = getpass("Elastic password: ")

es = Elasticsearch(
    cloud_id=ELASTIC_CLOUD_ID,  # cloud id can be found under deployment management
    basic_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD) # your username and password for connecting to elastic, found under Deplouments - Security
)

#Adding the models to your Elastic server must be done through docker, you can run the following code in your terminal with the desired model-ids of compatible third party models
#Examples with two types of models: sentiment analysis and embedding from HuggingFace
model_id = "sentence-transformers__msmarco-minilm-l-12-v3"
model_id = "distilbert-base-uncased-finetuned-sst-2-english"

'''
docker pull docker.elastic.co/eland/eland:8.9.0

docker run -it --rm elastic/eland \
    eland_import_hub_model \
      --cloud-id $ELASTIC_CLOUD_ID \
      -u $ELASTIC_USERNAME -p $ELASTIC_PASSWORD \
      --hub-model-id distilbert-base-uncased-finetuned-sst-2-english \
      --task-type text_classification \
      --start 
'''

#See all models successfuly imported into your instance
models = MlClient.get_trained_models(es)
for model in models["trained_model_configs"]:
    print(model["model_id"])


#Get info on a specific model
models = MlClient.get_trained_models(es, model_id=model_id)
models.body

#Run a query againt the model - this is the format the query imput must be used in, you can later map your features into this format through an ingest pipeline
doc_test = {"text_field": "This is a very nice sentence"}

result = MlClient.infer_trained_model(es, model_id =model_id, docs = doc_test)
result["inference_results"]

#Creating a pipeline to run the model against an entire index, and add a property to that index based on inference results
#In this example we're creating a pipeline for a sentiment analysis model, adjust this for your selected model
es.ingest.put_pipeline(
    id="sentiment", 
    processors=[
    {
      "inference": {
        "model_id": model_id,
        "target_field" : id,
        "field_map": {
          "Sentence": "text_field"
        }
      }
    }
  ]
)

#For the new enriched index, we need to add a field to the mappings where the inference results will be stored. 
#Here are two examples for sentiment and embeddings
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
            },
            "sentiment": {
                "properties": {
                    "model_id": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                            }
                        }},
                    "predicted_value": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                            }
                        }},
                    "prediction_probability": {
                        "type": "float"
                        }
                }
            },
            "text_embedding.predicted_value": {
                "type": "dense_vector",
                "dims": 384,
                "index": True,
                "similarity": "cosine"
            },
        }}

#Creating the new index with enriched data
es.indices.create(index=index, mappings=mappings)
es.reindex(body={
      "source": {
          "index": "index_name"},
      "dest": {"index": "index_name_new", "pipeline" : "sentiment"}
    }, wait_for_completion=False)

#An example searching using the new sentiment field
query={
    "match" : {
      "sentiment.predicted_value": "NEGATIVE"
    }
  }
response = es.search(index = "index_name_new",query=query, sort="sentiment.prediction_probability:desc")
print("The most negative sentences in the series:")
for hit in response["hits"]["hits"]:
    print(hit['_source']["Sentence"],  hit['_source']["sentiment"]["prediction_probability"] )



#An example searching using the new embeddings field
#In this case we also have to first convert the query text to the same embeddings space by also running this sentence against our inference model
question = "what languages do you use"
question_embedded = MlClient.infer_trained_model(es, model_id =model_id, docs = question)
query_vector = question_embedded["inference_results"][0]["predicted_value"]

query = {
        "field": "text_embedding.predicted_value",
        "query_vector": query_vector,
        "k": 5,
        "num_candidates": 100
        }
        
result = es.search(index = index, knn=query, source=["Sentence", "Character"])
print("{}: {}, score {}".format(result["_source"]["Name"], result["_source"]["Sentence"], result["_score"]))