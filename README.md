# 🎯 Goal

Through this unit's challenges you will design a data mart of your own! But to do that we will need some data.

AdventureWorks is a full database example provided by Microsoft and representing a made up bike company AdventureWorks Cycles. We will begin by cleaning the data a bit, creating a dataset and tables in BigQuery, uploading the data to BigQuery, and then work on creating some usable data marts!

The goal of this challenge is to:
- Download the data
- Process the data so it is in a useful format
- Create a BigQuery Dataset and Tables
- Upload the processed data into BigQuery

<br>

# 0️⃣ Download data

First, download the data from the Microsoft Github repository:

```bash
curl -o AdventureWorks2025.zip https://wagon-public-datasets.s3.amazonaws.com/data-engineering/AdventureWorks2025.zip
```

Create a `data` folder and unzip the data into it:

```bash
mkdir -p data/original && unzip AdventureWorks2025.zip
```
<!-- AdventureWorks2025.zip has the structure of data/original/*.csv because I mistyped the zip command -->

We need to do some pre-processing on the CSV's, luckily there is a script to convert **most** of the CSV's to a more usable format.

```bash
mkdir -p data/processed && python pipeline/process_csvs.py
```

This script will create two directories: `data/processed` and `data/processed_xml` - the fully refined data we want to bulk load into our data warehouse is in `data/processed_xml`.

We are going to focus primarily on sales to limit ourselves. There is one CSV that is not quite right. Have a look at `data/processed/store.csv`, what do you think is wrong with it?

<details>
<summary markdown='span'>💡 Hint</summary>

The fourth column is formatted as `XML`, not a very useable format for us! We will need to process this column into separate columns before we can upload it to BigQuery.

</details>

<br>

# 1️⃣ Fix store.csv!

Checkout the `pipeline/process_store.py`. The goal is to read data from `./data/processed/store.csv`, process the XML data, and save the processed output to `./data/processed_xml/store.csv`. Let's break down the steps to get there.

1. Finish the `parse_xml_to_dict` function. You can check how the function is working using the `__main__` block, which should output a dictionary with keys and values. Try using the imported ET module.

    <details>
    <summary markdown='span'>💡 Processed dictionary</summary>

    The built in python **pprint** library, [docs at this link](https://docs.python.org/3/library/pprint.html), might help you visualize terminal outputs!

    ```python
    {
        '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}AnnualSales': '3000000',
        '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}AnnualRevenue': '300000',
        '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}BankName': 'Primary Bank & Reserve',
        '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}BusinessType': 'OS',
        '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}YearOpened': '1974',
        '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}Specialty': 'Mountain',
        '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}SquareFeet': '75000',
        '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}Brands': '2',
        '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}Internet': 'T1',
        '{http://schemas.microsoft.com/sqlserver/2004/07/adventure-works/StoreSurvey}NumberEmployees': '93'
    }
    ```

    </details>

2. Update the `main` function in `process_store.py` to use the `parse_xml_to_dict` function. You should create a new CSV with the outfile by adding each of the values from the dict as columns at the **end** of the CSV and then removing the XML column!

3. Update the `__main__` block to run the `main` function and check that the output CSV in `./data/processed_xml/Store.csv` looks correct! The first row should look like this:

    ```csv
    292	Next-Door Bike Store	279	A22517E3-848D-4EBE-B9D9-7437F3432304	2025-09-11 11:15:07.497	800000	80000	United Security	BM	1996	Mountain	21000	2	ISDN	13
    ```

That's all the cleaning we're going to do for now. Let's move onto creating our data warehouse assets.

🧪 To test you have processed the CSV's, run:

```bash
make test_process_store
```

<details>
<summary markdown='span'>💡 Warnings on my tests!</summary>

Feel free to alter the `Makefile` to view the warnings and see if they are anything to worry about!

</details>

<br>

# 2️⃣ Create Warehouse Dataset and Tables

Let's create a BigQuery dataset to put our tables in before moving onto uploading our data!

1. Create a dataset named after your `BIGQUERY_DATASET` environment variable, set in your `.env`, in the EU region using the `bq` CLI command.

    <details>
    <summary markdown='span'>🎁 Solution</summary>

    ```bash
    bq --location=EU mk --dataset $BIGQUERY_DATASET
    ```
    </details>

2. Have a look at `pipeline/schemas.py`. You should see the schema for all of the tables we need to create, describing the columns, data type, and nullable metadata for each table. Now that `store.csv` is processed, they are related to sales and in a useable format. However we still need to make some editing to add the new columns from the XML processing!

    <details>
    <summary markdown='span'>💡 Completed store schema</summary>

    ```python
    "Store": [
        {"name": "BusinessEntityID", "type": "INT64", "mode": "REQUIRED"},
        {"name": "Name", "type": "STRING", "mode": "REQUIRED"},
        {"name": "SalesPersonID", "type": "INT64", "mode": "NULLABLE"},
        {'name': 'rowguid', 'type': 'STRING', 'mode': 'REQUIRED'},
        {"name": "ModifiedDate", "type": "TIMESTAMP", "mode": "REQUIRED"},
        {"name": "AnnualSales", "type": "FLOAT64", "mode": "REQUIRED"},
        {"name": "AnnualRevenue", "type": "FLOAT64", "mode": "REQUIRED"},
        {"name": "BankName", "type": "STRING", "mode": "REQUIRED"},
        {"name": "BusinessType", "type": "STRING", "mode": "REQUIRED"},
        {"name": "YearOpened", "type": "INT64", "mode": "REQUIRED"},
        {"name": "Specialty", "type": "STRING", "mode": "REQUIRED"},
        {"name": "SquareFeet", "type": "INT64", "mode": "REQUIRED"},
        {"name": "Brands", "type": "STRING", "mode": "REQUIRED"},
        {"name": "Internet", "type": "STRING", "mode": "REQUIRED"},
        {"name": "NumberEmployees", "type": "INT64", "mode": "REQUIRED"},
    ],
    ```
    </details>

3. We want to create the tables algorithmically using the data defined in `schemas.py`

❓ Complete the inside of the loop of `main` inside `pipeline/create_tables.py` to create the tables using the schemas!

Once you think you have it working, run the script and have a look at the tables that were created in BigQuery!

<details>
<summary markdown='span'>❗ Incorrect dataset or table names</summary>
No stress, delete the dataset and/or table through the BigQuery console and try again.
</details>

🧪 To test you have created the BigQuery dataset and tables, run:

```bash
make test_bq_assets
```

<br>

# 3️⃣ Upload the data

Now that we have all the data locally and the tables created in our warehouse, we want load all our local data into the tables!

1. Checkout the `pipeline/upload_data.py`. You should see the `main` function has a loop that iterates over the schema.

2. Complete the loop to upload the data in each CSV in `./data/processed_xml` to the correct table!

3. When you think you have it working, run the script and check the data has been uploaded!

<br>

# 4️⃣ Query the data

Now that we have the data in the table, we can start to query it! An easy way to do this is through the BigQuery interface. Just click on query at the top of the main panel and it will bring up a SQL editor.

Alternatively you can query from the command line with the `bq` CLI tool:

```bash
bq query "SELECT * FROM adventure_works_raw.Store LIMIT 10;"
```

<br>

# 🏁 Finish

With all the data in our data warehouse, we're ready to create data marts in the next challenge!

🧪 Run `make test`, commit, and push your code to github so Kitt can track your progress!

<br>
