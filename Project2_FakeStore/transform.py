import pandas as pd

def validate_data(df: pd.DataFrame) -> bool:
    """מבצעת בדיקות אמינות ואיכות נתונים (Data Quality Checks)"""
    if df is None or df.empty:
        print("❌ Validation Failed: DataFrame is empty.")
        return False

    # 1. בדיקת כפילויות ב-ID
    if df['id'].duplicated().any():
        print("❌ Validation Failed: Duplicate IDs found.")
        return False

    # 2. בדיקת מחירים לא חוקיים (שליליים או אפס)
    if (df['price'] <= 0).any():
        print("❌ Validation Failed: Found products with invalid price (<= 0).")
        return False

    # 3. בדיקת ערכים חסרים בשדות קריטיים
    if df[['id', 'title', 'category']].isnull().any().any():
        print("❌ Validation Failed: Missing values in critical columns.")
        return False

    print("✅ Data Quality Checks passed successfully!")
    return True

def transform_data(raw_data):
    """מנקה ומעבד נתונים גולמיים מ-API"""
    if not raw_data:
        print("No data provided for transformation.")
        return None

    df = pd.DataFrame(raw_data)

    # בחירת עמודות
    df = df[['id', 'title', 'price', 'category', 'rating']]

    # חילוץ אובייקט פנימי
    df['rating_rate'] = df['rating'].apply(lambda x: x.get('rate') if isinstance(x, dict) else None)
    df['rating_count'] = df['rating'].apply(lambda x: x.get('count') if isinstance(x, dict) else None)
    df = df.drop(columns=['rating'])

    # עמודה מחושבת
    df['price_with_vat'] = (df['price'] * 1.18).round(2)

    # הרצת בדיקות האיכות
    if not validate_data(df):
        raise ValueError("Data validation failed. Aborting pipeline process.")

    print(f"Successfully transformed and validated {len(df)} records.")
    return df