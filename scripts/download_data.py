# scripts/download_data.py
import pandas as pd
import os

def download_wine_data():
    """Download wine quality dataset from UCI repository"""
    
    print("Downloading wine quality dataset...")
    
    # URL for red wine quality dataset
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv"
    
    # Download and read the data
    df = pd.read_csv(url, sep=';')
    
    # Create directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Save to CSV
    output_path = 'data/raw/wine_quality.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✓ Downloaded successfully!")
    print(f"✓ Saved to: {output_path}")
    print(f"✓ Total samples: {len(df)}")
    print(f"✓ Features: {len(df.columns)}")
    print(f"✓ Columns: {', '.join(df.columns.tolist())}")
    
    # Show first few rows
    print("\nFirst 3 rows:")
    print(df.head(3))

if __name__ == '__main__':
    download_wine_data()