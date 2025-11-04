# scripts/feature_engineering.py
import pandas as pd
import numpy as np

def engineer_features():
    """Create new features from cleaned wine data"""
    
    print("Loading cleaned data...")
    df = pd.read_csv('data/processed/wine_quality_clean.csv')
    print(f"Starting dataset: {len(df)} samples, {len(df.columns)} features")
    
    # Create new features
    print("\n Creating new features...")
    
    # 1. Total Acidity
    df['total_acidity'] = df['fixed acidity'] + df['volatile acidity']
    print("    total_acidity = fixed acidity + volatile acidity")
    
    # 2. Alcohol to Density Ratio
    df['alcohol_to_density'] = df['alcohol'] / df['density']
    print("    alcohol_to_density = alcohol / density")
    
    # 3. Sulphates to Alcohol Ratio
    df['sulphates_to_alcohol'] = df['sulphates'] / df['alcohol']
    print("    sulphates_to_alcohol = sulphates / alcohol")
    
    # 4. Acidity Ratio
    df['acidity_ratio'] = df['fixed acidity'] / (df['volatile acidity'] + 0.001)  # Add small value to avoid division by zero
    print("    acidity_ratio = fixed acidity / volatile acidity")
    
    # 5. Free to Total Sulfur Ratio
    df['free_to_total_sulfur'] = df['free sulfur dioxide'] / (df['total sulfur dioxide'] + 0.001)
    print("    free_to_total_sulfur = free sulfur dioxide / total sulfur dioxide")
    
    # 6. Binary quality classification (good wine: quality >= 7)
    df['is_good_quality'] = (df['quality'] >= 7).astype(int)
    print("    is_good_quality = 1 if quality >= 7, else 0")
    
    # Summary
    print(f"\n Feature engineering complete!")
    print(f" Original features: 12")
    print(f" New features: 6")
    print(f" Total features: {len(df.columns)}")
    
    # Save feature-engineered data
    output_path = 'data/features/wine_quality_featured.csv'
    df.to_csv(output_path, index=False)
    print(f" Saved to: {output_path}")
    
    # Show feature statistics
    print("\nNew features summary:")
    new_features = ['total_acidity', 'alcohol_to_density', 'sulphates_to_alcohol', 
                    'acidity_ratio', 'free_to_total_sulfur', 'is_good_quality']
    print(df[new_features].describe())
    
    # Show good quality distribution
    print(f"\nGood quality wines (quality >= 7): {df['is_good_quality'].sum()}")
    print(f"Regular quality wines (quality < 7): {len(df) - df['is_good_quality'].sum()}")

if __name__ == '__main__':
    engineer_features()