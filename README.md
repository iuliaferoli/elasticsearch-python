# Python <3 Elasticsearch
A collection of Elasticsearch examples and use cases; use as a reference or cheat sheet for working with python + elastic

## Starting out with Elasticsearch
- [X] Connect to the Elastic server, create an index, add documents, run a simple query.
[notebook](/Simple%20Query.ipynb)

## Getting Data into Elasticsearch
- [X] [Loading data](loading_data.py)
- [X] [Using parallel_bulk](using_parallel_bulk.py) 
- [X] Perform actions when ingesting data, for example an ingest pipeline adding a timestamp any time a document is updated. [notebook](/Ingest%20pipelines%20with%20timestamps.ipynb)

## Machine Learning
- [X] Build a simple classifier with the `more like this` query without any ML. [notebook](/Classifier%20with%20MLT%20Query.ipynb)
- [X] Importing NLP third party models (LLMs) or ELSER and performing searches based on semantic data.
[notebook](/Elastic%20LLM%20Models%20and%20Semantic%20Search.ipynb)
- [ ] Huggingface Examples
- [X] [Langchain Examples](/Langchain%20Chains%20Example.ipynb)



- [ ] Observability & Tracking
