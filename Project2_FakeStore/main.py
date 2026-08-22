from extract import fetch_data
from transform import transform_data
from load import load_data

def run_pipeline():
    print("--- Starting FakeStore ETL Pipeline ---")
    
    # 1. Extract
    print("Step 1: Extracting raw data from API...")
    raw_data = fetch_data()
    
    if not raw_data:
        print("Pipeline aborted: Extraction failed.")
        return

    # 2. Transform
    print("Step 2: Transforming data...")
    transformed_df = transform_data(raw_data)
    
    # 3. Load
    print("Step 3: Loading data to targets...")
    load_data(transformed_df)
    
    print("\nETL Pipeline completed successfully מקצה לקצה!")

if __name__ == "__main__":
    run_pipeline()