import os
from google.cloud import bigquery
import pandas as pd
from transform import transform_data
from extract import fetch_data

def load_data_to_bigquery():
    # 1. הגדרת נתיב למפתח הגישה
    key_path = os.path.join(os.path.dirname(__file__), "gcp-key.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

    # 2. אתחול לקוח BigQuery
    client = bigquery.Client()

    # 🛑 שנה את YOUR_PROJECT_ID לשם הפרויקט המדויק שלך ב-GCP!
    project_id = "data-engineer-project-506311" 
    table_id = f"{project_id}.fakestore_dw.products"

    print("Fetching and transforming data...")
    raw_data = fetch_data()
    df = transform_data(raw_data)

    # 3. הגדרת תצורת הטעינה (Overwrite בכל הרצה)
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )

    print(f"Uploading {len(df)} rows to BigQuery table: {table_id}...")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()  # ממתין לסיום הפעולה

    print("✅ Data successfully loaded to BigQuery!")

if __name__ == "__main__":
    load_data_to_bigquery()