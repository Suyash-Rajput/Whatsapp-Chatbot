import os
from google.cloud import bigquery

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/content/autotask-loreal-dv-dd0494ce10d7.json'


client = bigquery.Client()


def create_dataset() :
    f