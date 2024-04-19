import os
from google.cloud import bigquery

class  GCP_big_query():
 
    def __init__(self):
        self.client = bigquery.Client()
        self.schema = [
            bigquery.SchemaField("message_sender", "STRING"),
            bigquery.SchemaField("message_receiver", "STRING"),
            bigquery.SchemaField("message_time", "TIMESTAMP"),
            bigquery.SchemaField("message_text", "STRING"),
        ]
    
    def get_existing_rows(self, table_id, dataset_id):
        table_ref = self.client.dataset(dataset_id).table(table_id)
        table = self.client.get_table(table_ref)
        rows = self.client.list_rows(table)
        row_count = sum(1 for row in rows)
        return row_count
         
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
        try:
           self.client.get_table(table_ref)
           print(f"Table '{table_id}' already exists.")
        except Exception as e:
            table = bigquery.Table(table_ref, schema=self.schema)
            self.client.create_table(table)
            print(f"Table '{table_id}' created successfully.")
    
    
    def insert_data(self, rows_to_insert, table_id, dataset_id):
        table = bigquery.Table(f'autotask-loreal-dv.Chatbot_messages_dataset.{table_id}', schema= self.schema)
        table = self.client.create_table(table, exists_ok=True)
        inserted = self.client.insert_rows_json(dataset_id + '.' + table_id,rows_to_insert)
        if inserted == []:
            print("Data successfully inserted into BigQuery table.")
        else:
            print("Encountered errors while inserting data into BigQuery table:", inserted)


    def retrieve(self, table_id, dataset_id, company_name):
        sql_query = f"SELECT * FROM `{dataset_id}.{table_id}`"
        sql_query = f"""
            SELECT *
            FROM `{dataset_id}.{table_id}`
            WHERE company_name = "{company_name}"
            """
        query_job = self.client.query(sql_query)
        print("Retrieved data:")
        rows = []
        for row in query_job:
            rows.append(row)
        return rows


    def delete_dataset(self, dataset_id):
        try:
            self.client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)
            print(f"Dataset '{dataset_id}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting dataset '{dataset_id}': {e}")
