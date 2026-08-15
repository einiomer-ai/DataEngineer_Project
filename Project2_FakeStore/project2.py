import sqlite3
import pandas as pd
import requests

# ==========================================
# 1. EXTRACT (שאיבת הנתונים)
# ==========================================
url = "https://fakestoreapi.com/products"
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)

# ==========================================
# 2. TRANSFORM (שיטוח, בחירת עמודות וסינון)
# ==========================================
# א. שיטוח העמודה המורכבת rating
df["rating_score"] = df["rating"].apply(lambda x: x["rate"])
df["rating_count"] = df["rating"].apply(lambda x: x["count"])

# ב. בחירת עמודות רלוונטיות בלבד
clean_df = df[
    [
        "id",
        "title",
        "price",
        "category",
        "rating_score",
        "rating_count",
    ]
].copy()

# ג. הסינון שכתבת: רק מוצרים שמחירם מעל 50
filtered_df = clean_df[clean_df["price"] > 50]

print("=== 3 השורות הראשונות של הדאטה המסונן ===")
print(filtered_df.head(3))

# ==========================================
# 3. LOAD (אחסון ב-Parquet וטעינה ל-SQL)
# ==========================================
# א. שמירה ב-Data Lake (פורמט Parquet)
filtered_df.to_parquet("expensive_products.parquet", index=False)
print("\n1. נשמר בהצלחה לקובץ Parquet!")

# ב. טעינה ל-Data Warehouse (SQLite)
conn = sqlite3.connect("store_data.db")
filtered_df.to_sql("products", conn, if_exists="replace", index=False)
print("2. הנתונים נטענו בהצלחה לטבלת SQL בשם 'products'!")



# ג. בדיקת שליפה מתוך ה-SQL
sql_check = pd.read_sql("SELECT category, COUNT(*) as product_count FROM products GROUP BY category", conn)
print("\n=== סיכום מוצרים יקרים לפי קטגוריה (מתוך ה-SQL) ===")
print(sql_check)

conn.close()

category_counts = filtered_df.groupby('category')['id'].count()
print(category_counts)

category_avg_price= filtered_df.groupby('category')['price'].mean()
print(category_avg_price)

category_summary = filtered_df.groupby('category')['price'].aggregate(['max','count','mean'])
print(category_summary)