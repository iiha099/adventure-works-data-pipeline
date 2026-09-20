from pipeline.schemas import bigquery_schemas
from google.cloud import bigquery
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    """
    Main function to take the bigquery schemas and create the tables in the raw dataset.
    """
    client = bigquery.Client()
    dataset_name = os.environ.get("BIGQUERY_DATASET")

    for table_name, schema in bigquery_schemas.items():
        table_id = f"{client.project}.{dataset_name}.{table_name}"
        table = bigquery.Table(table_id, schema=schema)
        client.create_table(table, exists_ok=True)
        print(f"Created table: {table_name}")


if __name__ == "__main__":
    main()
