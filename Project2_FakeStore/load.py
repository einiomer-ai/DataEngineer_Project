import sqlite3
import pandas as pd

def load_data(df: pd.DataFrame, db_path="store_data.db", parquet_path="transformed_products.parquet"):
    """טוען את ה-DataFrame לקובץ Parquet ולטבלת SQLite"""
    try:
        # 1. שמירה ב-Data Lake (Parquet)
        df.to_parquet(parquet_path, index=False)
        print(f"Data saved to Parquet file: '{parquet_path}'")

        # 2. טעינה ל-Data Warehouse (SQLite)
        conn = sqlite3.connect(db_path)
        df.to_sql("products", conn, if_exists="replace", index=False)
        conn.close()
        print(f"Data successfully loaded to SQLite table 'products' in '{db_path}'")

    except Exception as e:
        print(f"Error during Load phase: {e}")