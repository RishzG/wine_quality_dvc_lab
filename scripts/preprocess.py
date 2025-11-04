# scripts/preprocess.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def preprocess_wine_data():
    """Clean and preprocess wine quality dataset"""
    
    print("Loading raw data...")
    df = pd.read_csv('data/raw/wine_quality.csv')
    print(f"Original dataset: {len(df)} samples, {len(df.columns)} features")
    
    # Step 1: Remove duplicates
    print("\n1. Removing duplicates...")
    original_count = len(df)
    df = df.drop_duplicates()
    print(f"   Removed {original_count - len(df)} duplicates")
    print(f"   Remaining: {len(df)} samples")
    
    # Step 2: Remove outliers using IQR method
    print("\n2. Removing outliers (IQR method)...")
    original_count = len(df)
    
    for col in df.columns[:-1]:  # All columns except 'quality'
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    
    print(f"   Removed {original_count - len(df)} outliers")
    print(f"   Remaining: {len(df)} samples")
    
    # Step 3: Normalize features (except quality)
    print("\n3. Normalizing features...")
    scaler = StandardScaler()
    feature_cols = df.columns[:-1]  # All except 'quality'
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    print(f"    Normalized {len(feature_cols)} features")
    
    # Step 4: Save processed data
    output_path = 'data/processed/wine_quality_clean.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n Preprocessing complete!")
    print(f" Saved to: {output_path}")
    print(f" Final dataset: {len(df)} samples, {len(df.columns)} features")
    
    # Show summary statistics
    print("\nQuality distribution:")
    print(df['quality'].value_counts().sort_index())

if __name__ == '__main__':
    preprocess_wine_data()