import pandas as pd

sales = pd.read_csv("sales.csv")

# הצגת כל הנתונים
print("כל המכירות:")
print(sales)

# סינון מכירות מעל 2000
high_sales = sales[sales["amount"] > 2000]

print("\nמכירות מעל 2000:")
print(high_sales)

# סכום כל המכירות
total_sales = sales["amount"].sum()

print("\nסך המכירות:")
print(total_sales)

# המוצר עם המכירה הגבוהה ביותר
max_sale = sales.loc[sales["amount"].idxmax()]

print("\nהמכירה הגבוהה ביותר:")
print(max_sale)

print("\nColumns:")
print(sales.columns)

print("\nData types:")
print(sales.dtypes)

print("\nNumber of rows:")
print(len(sales))