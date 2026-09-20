from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import pytest
import os
from pipeline.schemas import bigquery_schemas
from dotenv import load_dotenv
load_dotenv()


@pytest.fixture(scope="module")
def bigquery_client():
    return bigquery.Client()


def dataset_exists(client, bq_dataset):
    datasets = list(client.list_datasets())
    try:
        if datasets:
            datasets = [dataset.dataset_id for dataset in datasets]
            if bq_dataset in datasets:
                return True
    except NotFound:
        return


def get_bq_tables(client, dataset_id):
    tables = client.list_tables(dataset_id)
    try:
        if tables:
            tables = [table.table_id for table in tables]
            return sorted(tables)
    except NotFound:
        return


def test_bigquery_dataset_exists(bigquery_client):
    bq_dataset = os.environ.get("BIGQUERY_DATASET")
    assert dataset_exists(
        bigquery_client, bq_dataset
    ), "Dataset 'raw' does not exist in BigQuery, make sure it's been created!"


def test_bigquery_table_exists(bigquery_client):
    project_id = os.environ.get("PROJECT_ID")
    bq_dataset = os.environ.get("BIGQUERY_DATASET")

    dataset_id = f"{project_id}.{bq_dataset}"
    schema_tables = sorted(list(bigquery_schemas.keys()))
    bq_tables = get_bq_tables(bigquery_client, dataset_id)
    assert (
        schema_tables == bq_tables
    ), "Check all the tables have been created in BigQuery!"
