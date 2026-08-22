import requests

def fetch_data():
    """מביא נתונים גולמיים מה-API של FakeStore"""
    url = "https://fakestoreapi.com/products"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None