# scripts/analyze_versions.py
import pandas as pd
import json
import os

def analyze_dataset(file_path, version_name):
    """Analyze a dataset version and return statistics"""
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found")
        return None
    
    df = pd.read_csv(file_path)
    
    stats = {
        'version': version_name,
        'num_samples': int(len(df)),
        'num_features': int(len(df.columns)),
        'file_size_kb': round(os.path.getsize(file_path) / 1024, 2),
        'missing_values': int(df.isnull().sum().sum()),
        'columns': df.columns.tolist()
    }
    
    # Add quality distribution if quality column exists
    if 'quality' in df.columns:
        quality_dist = df['quality'].value_counts().sort_index().to_dict()
        stats['quality_distribution'] = {int(k): int(v) for k, v in quality_dist.items()}
    
    # Add good quality count if it exists
    if 'is_good_quality' in df.columns:
        stats['good_quality_count'] = int(df['is_good_quality'].sum())
        stats['regular_quality_count'] = int(len(df) - df['is_good_quality'].sum())
    
    return stats

def main():
    """Analyze all dataset versions"""
    
    print("=" * 60)
    print("WINE QUALITY DATASET - VERSION ANALYSIS")
    print("=" * 60)
    
    # Define versions to analyze
    versions = {
        'v1_raw': 'data/raw/wine_quality.csv',
        'v2_clean': 'data/processed/wine_quality_clean.csv',
        'v3_features': 'data/features/wine_quality_featured.csv'
    }
    
    all_stats = {}
    
    # Analyze each version
    for version, path in versions.items():
        print(f"\nAnalyzing {version}...")
        stats = analyze_dataset(path, version)
        
        if stats:
            all_stats[version] = stats
            print(f"  Samples: {stats['num_samples']}")
            print(f"   Features: {stats['num_features']}")
            print(f"   Size: {stats['file_size_kb']} KB")
            print(f"   Missing values: {stats['missing_values']}")
    
    # Save statistics to JSON
    os.makedirs('reports', exist_ok=True)
    output_file = 'reports/dataset_stats.json'
    
    with open(output_file, 'w') as f:
        json.dump(all_stats, f, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f" Analysis complete")
    print(f" Statistics saved to: {output_file}")
    print(f"{'=' * 60}")
    
    # Print summary comparison
    print("\nSUMMARY COMPARISON:")
    print("-" * 60)
    print(f"{'Version':<15} {'Samples':<10} {'Features':<10} {'Size (KB)':<12}")
    print("-" * 60)
    
    for version, stats in all_stats.items():
        print(f"{version:<15} {stats['num_samples']:<10} {stats['num_features']:<10} {stats['file_size_kb']:<12}")
    
    print("-" * 60)
    
    # Calculate changes
    if 'v1_raw' in all_stats and 'v2_clean' in all_stats:
        sample_reduction = all_stats['v1_raw']['num_samples'] - all_stats['v2_clean']['num_samples']
        reduction_pct = (sample_reduction / all_stats['v1_raw']['num_samples']) * 100
        print(f"\nData cleaning removed {sample_reduction} samples ({reduction_pct:.1f}% reduction)")
    
    if 'v2_clean' in all_stats and 'v3_features' in all_stats:
        feature_increase = all_stats['v3_features']['num_features'] - all_stats['v2_clean']['num_features']
        increase_pct = (feature_increase / all_stats['v2_clean']['num_features']) * 100
        print(f"Feature engineering added {feature_increase} features ({increase_pct:.1f}% increase)")
    
    if 'v3_features' in all_stats and 'good_quality_count' in all_stats['v3_features']:
        good = all_stats['v3_features']['good_quality_count']
        total = all_stats['v3_features']['num_samples']
        print(f"Good quality wines: {good}/{total} ({(good/total*100):.1f}%)")

if __name__ == '__main__':
    main()