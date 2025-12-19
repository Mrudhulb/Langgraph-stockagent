import pandas as pd
import requests
from io import StringIO

def get_gainers():
    url = "https://finance.yahoo.com/gainers"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print(f"Fetching {url}...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse tables
        print("Parsing HTML...")
        tables = pd.read_html(StringIO(response.text))
        
        if not tables:
            print("No tables found.")
            return []
            
        # Usually the first table is the gainers list
        df = tables[0]
        print("\nColumns found:", df.columns.tolist())
        
        # Extract tickers (Symbol column)
        tickers = df['Symbol'].head(5).tolist()
        print("\nTop 5 Gainers:", tickers)
        return tickers
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    get_gainers()
