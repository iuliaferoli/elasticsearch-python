import pandas as pd
from getpass import getpass
from elasticsearch import Elasticsearch, helpers

repair_data_df = pd.read_csv('/path/to/OpenRepairData_v0.3_RepairCafeInt_202309.csv')
repair_data_df = repair_data_df.fillna(0)
print(repair_data_df.head())

elastic_cloud_id = getpass("Elastic Cloud ID: ")
elastic_api_key = getpass("API Key: ")

es = Elasticsearch(cloud_id=elastic_cloud_id, api_key=elastic_api_key)

index_name = 'repair'
es.indices.create(index=index_name)


def df_to_doc(df, name_of_index):
    for index, document in df.iterrows():
        yield dict(_index=name_of_index, _id=f"{document['id']}", _source=document.to_dict())


helpers.bulk(es, df_to_doc(repair_data_df, index_name))