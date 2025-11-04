# scripts/visualize_evolution.py
import json
import matplotlib.pyplot as plt
import os

def load_stats():
    """Load statistics from JSON file"""
    with open('reports/dataset_stats.json', 'r') as f:
        return json.load(f)

def create_visualizations():
    """Create comparison visualizations for all dataset versions"""
    
    print("Loading statistics...")
    stats = load_stats()
    
    # Extract data for plotting
    versions = list(stats.keys())
    samples = [stats[v]['num_samples'] for v in versions]
    features = [stats[v]['num_features'] for v in versions]
    sizes = [stats[v]['file_size_kb'] for v in versions]
    
    # Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Wine Quality Dataset Evolution', fontsize=16, fontweight='bold')
    
    # Color scheme
    colors = ['#3498db', '#2ecc71', '#e74c3c']
    
    # Plot 1: Sample count
    axes[0].bar(versions, samples, color=colors, alpha=0.7, edgecolor='black')
    axes[0].set_title('Number of Samples', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Count', fontsize=10)
    axes[0].grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, (v, s) in enumerate(zip(versions, samples)):
        axes[0].text(i, s + 20, str(s), ha='center', va='bottom', fontweight='bold')
    
    # Plot 2: Feature count
    axes[1].bar(versions, features, color=colors, alpha=0.7, edgecolor='black')
    axes[1].set_title('Number of Features', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Count', fontsize=10)
    axes[1].grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, (v, f) in enumerate(zip(versions, features)):
        axes[1].text(i, f + 0.3, str(f), ha='center', va='bottom', fontweight='bold')
    
    # Plot 3: File size
    axes[2].bar(versions, sizes, color=colors, alpha=0.7, edgecolor='black')
    axes[2].set_title('File Size (KB)', fontsize=12, fontweight='bold')
    axes[2].set_ylabel('Size (KB)', fontsize=10)
    axes[2].grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, (v, s) in enumerate(zip(versions, sizes)):
        axes[2].text(i, s + 2, f'{s:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure
    output_file = 'reports/version_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f" Visualization saved to: {output_file}")
    
    # Create quality distribution plot if available
    if 'quality_distribution' in stats['v1_raw']:
        create_quality_distribution(stats)
    
    print(" All visualizations complete!")

def create_quality_distribution(stats):
    """Create quality distribution comparison"""
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Quality Distribution Across Versions', fontsize=16, fontweight='bold')
    
    versions = ['v1_raw', 'v2_clean', 'v3_features']
    titles = ['v1.0: Raw Data', 'v2.0: Cleaned Data', 'v3.0: Feature-Engineered']
    
    for i, (version, title) in enumerate(zip(versions, titles)):
        if version in stats and 'quality_distribution' in stats[version]:
            quality_dist = stats[version]['quality_distribution']
            qualities = sorted(quality_dist.keys())
            counts = [quality_dist[q] for q in qualities]
            
            axes[i].bar(qualities, counts, color='#3498db', alpha=0.7, edgecolor='black')
            axes[i].set_title(title, fontsize=11, fontweight='bold')
            axes[i].set_xlabel('Quality Rating', fontsize=9)
            axes[i].set_ylabel('Count', fontsize=9)
            axes[i].grid(axis='y', alpha=0.3, linestyle='--')
            
            # Add value labels
            for q, c in zip(qualities, counts):
                axes[i].text(q, c + 5, str(c), ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('reports/quality_distribution.png', dpi=300, bbox_inches='tight')
    print(f" Quality distribution saved to: reports/quality_distribution.png")

if __name__ == '__main__':
    create_visualizations()