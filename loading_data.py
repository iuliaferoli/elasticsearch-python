# Import necessary libraries
import pandas as pd  # For data manipulation with DataFrames
from getpass import getpass  # For securely getting user input (passwords)
from elasticsearch import Elasticsearch, helpers  # For interacting with Elasticsearch

# Read data from a CSV file into a DataFrame
# The Repair Cafe International dataset can be downloaded at https://openrepair.org/open-data/downloads/
repair_data_df = pd.read_csv('/path/to/OpenRepairData_v0.3_RepairCafeInt_202309.csv')

# Fill missing values in the DataFrame with 0
repair_data_df = repair_data_df.fillna(0)

# Print the first few rows of the DataFrame to inspect the data
print(repair_data_df.head())

# Prompt the user to enter their Elastic Cloud ID and API Key securely
elastic_cloud_id = getpass("Elastic Cloud ID: ")
elastic_api_key = getpass("API Key: ")

# Create an Elasticsearch client using the provided credentials
es = Elasticsearch(cloud_id=elastic_cloud_id, api_key=elastic_api_key)

# Define the name of the Elasticsearch index to be created
index_name = 'repair'

# Create the Elasticsearch index with the specified name
es.indices.create(index=index_name)


# Define a function to convert DataFrame rows to Elasticsearch documents
def df_to_doc(df, name_of_index):
    for index, document in df.iterrows():
        yield dict(_index=name_of_index, _id=f"{document['id']}", _source=document.to_dict())


# Use the Elasticsearch helpers.bulk() method to index the DataFrame data into Elasticsearch
load = helpers.bulk(es, df_to_doc(repair_data_df, index_name))
print(load)
