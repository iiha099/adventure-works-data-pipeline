from google.cloud import bigquery
from pipeline.schemas import bigquery_schemas
import os

from dotenv import load_dotenv
load_dotenv()

def rename_type_to_field_type(schema_dict):
    for _, fields in schema_dict.items():
        for field in fields:
            if "type" in field:
                field["field_type"] = field.pop("type")
    return schema_dict


def main():
    client = bigquery.Client()

    dataset_name = os.environ.get("BIGQUERY_DATASET")

    updated_schemas = rename_type_to_field_type(bigquery_schemas)

    for table_name in bigquery_schemas.keys():
        # $CHALLENGIFY_BEGIN
        csv_file_path = f"data/processed_xml/{table_name}.csv"
        dataset_ref = bigquery.DatasetReference(client.project, dataset_name)
        table_ref = dataset_ref.table(table_name)

        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.CSV
        job_config.schema = [
            bigquery.SchemaField(**field) for field in updated_schemas[table_name]
        ]
        job_config.field_delimiter = "\t"

        with open(csv_file_path, "rb") as csv_file:
            job = client.load_table_from_file(
                csv_file,
                table_ref,
                job_config=job_config,
            )

        try:
            job.result()
            print(f"Loaded data into {table_name}")
        except Exception as e:
            print(f"Could not load data into {table_name}: {e}")
        # $CHALLENGIFY_END


if __name__ == "__main__":
    main()
