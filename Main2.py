import requests
import pandas as pd
import sqlite3


# 1. Extract
url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)
data = response.json()

# 2. Transform
df = pd.DataFrame(data)

df['city'] = df['address'].apply(lambda x: x['city'])
df['company_name'] = df['company'].apply(lambda x: x['name'])

clean_df = df[['id', 'name', 'email', 'city', 'company_name']].copy()
clean_df.rename(columns={'name': 'full_name'}, inplace=True)

# 3. Filter (כאן נבנה המשתנה filtered_df!)
filtered_df = clean_df[clean_df['city'].str.startswith('S')]

# 4. Load (שמירה לקובץ Parquet)
filtered_df.to_parquet('filtered_users.parquet', index=False)

print("הקובץ נשמר בהצלחה בפורמט Parquet!")


# 1. יצירת חיבור למסד נתונים קל (ייצור קובץ DB מקומי)
conn = sqlite3.connect('my_data_warehouse.db')

# 2. טעינת ה-DataFrame לתוך טבלת SQL בשם 'users'
filtered_df.to_sql('users', conn, if_exists='replace', index=False)

print("הנתונים נטענו בהצלחה לטבלת SQL!")

# 3. בדיקה: הרצת שאילתת SQL קלאסית כדי לוודא שהדאטה שם
query_result = pd.read_sql("SELECT full_name, city FROM users", conn)
print("\n--- תוצאת שאילתת ה-SQL מתוך הדאטהבייס ---")
print(query_result)

# סגירת החיבור
conn.close()
