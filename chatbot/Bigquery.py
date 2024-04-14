import os
from google.cloud import bigquery

class  GCP_big_query():
 
    def __init__(self):
        self.client = bigquery.Client()
        self.schema = [
            bigquery.SchemaField("id", "STRING"),
            bigquery.SchemaField("message_sender", "STRING"),
            bigquery.SchemaField("message_receiver", "STRING"),
            bigquery.SchemaField("message_time", "TIMESTAMP"),
            bigquery.SchemaField("message_text", "STRING"),
            bigquery.SchemaField("inserted_time", "TIMESTAMP"),
        ]

    def create_dataset(self,dataset_id):
        dataset_ref = self.client.dataset(dataset_id)
        dataset = bigquery.Dataset(dataset_ref)
        try:
            self.client.create_dataset(dataset)
            print(f"Dataset '{dataset_id}' created successfully.")
        except Exception as e:
            print(f"Dataset '{dataset_id}' already exists.")
            

    def create_table(self, table_id, dataset_id):
        dataset_ref = self.client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table =  bigquery.Table(table_ref, schema = self.schema)
        try:
            self.client.create_table(table)
            print(f"Table '{table_id}' created successfully.")
        except Exception as e:
            print(f"Table '{table_id}' already exists.")
    
    
    def insert_data(self, rows_to_insert, table_id, dataset_id):
        dataset_ref = self.client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)
        table =  bigquery.Table(table_ref, scheme = self.scheme)
        self.client.insert_rows(table, rows_to_insert)
        print("Data inserted into the table.")


    def retrieve(self, table_id, dataset_id):
        sql_query = f"SELECT * FROM `{dataset_id}.{table_id}`"
        query_job = self.client.query(sql_query)
        print("Retrieved data:")
        for row in query_job:
            print(row)


    def delete_dataset(self, dataset_id):
        try:
            self.client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
            print(f"Dataset '{dataset_id}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting dataset '{dataset_id}': {e}")
