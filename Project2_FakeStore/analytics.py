import sqlite3
import pandas as pd

def run_analytics():
    db_path = "store_data.db"
    
    try:
        conn = sqlite3.connect(db_path)
        print("=== 📊 FakeStore SQL Analytics ===\n")

        # 1. ניתוח לפי קטגוריות (Aggregations)
        query_categories = """
        SELECT 
            category,
            COUNT(id) AS total_products,
            ROUND(AVG(price), 2) AS avg_price,
            MIN(price) AS min_price,
            MAX(price) AS max_price,
            ROUND(AVG(rating_rate), 2) AS avg_rating
        FROM products
        GROUP BY category
        ORDER BY total_products DESC;
        """
        df_categories = pd.read_sql_query(query_categories, conn)
        print("--- 1. Category Summary ---")
        print(df_categories.to_string(index=False))
        print("\n" + "="*40 + "\n")

        # 2. המוצרים המובילים (Top Rated Products > 4.0)
        query_top_rated = """
        SELECT 
            title,
            category,
            price,
            rating_rate,
            rating_count
        FROM products
        WHERE rating_rate >= 4.0
        ORDER BY rating_rate DESC, rating_count DESC;
        """
        df_top_rated = pd.read_sql_query(query_top_rated, conn)
        print("--- 2. Top Rated Products (>= 4.0) ---")
        print(df_top_rated.to_string(index=False))
        print("\n" + "="*40 + "\n")

        # 3. סיכום הכנסות ושווי מלאי כולל מע"מ
        query_financials = """
        SELECT 
            COUNT(id) AS total_items,
            ROUND(SUM(price), 2) AS total_value_net,
            ROUND(SUM(price_with_vat), 2) AS total_value_gross,
            ROUND(SUM(price_with_vat - price), 2) AS total_vat_collected
        FROM products;
        """
        df_financials = pd.read_sql_query(query_financials, conn)
        print("--- 3. Financial Totals ---")
        print(df_financials.to_string(index=False))

        conn.close()

    except Exception as e:
        print(f"Error executing analytics query: {e}")

if __name__ == "__main__":
    run_analytics()