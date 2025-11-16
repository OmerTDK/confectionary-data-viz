#!/usr/bin/env python3
"""
Script to generate key visualizations for the README
Run this script to create images in the images/ directory
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8')
sns.set_theme()

# Load data
print("Loading data...")
df = pd.read_excel('confectionary.xlsx')
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

# Clean data
core_numeric = ['Units Sold', 'Cost(£)', 'Profit(£)', 'Revenue(£)']
df_clean = df.dropna(subset=['Units Sold', 'Cost(£)', 'Profit(£)']).copy()
df_clean['Profit_Margin'] = df_clean['Profit(£)'] / df_clean['Revenue(£)']

# Fix confectionary names
conf_mapping = {
    'Choclate Chunk': 'Chocolate Chunk',
    'Caramel nut': 'Caramel Nut',
}
df_clean['Confectionary_clean'] = df_clean['Confectionary'].replace(conf_mapping)

# Regional summary
print("Creating regional summary...")
regional_summary = df_clean.groupby('Country(UK)', as_index=False).agg({
    'Units Sold': 'sum',
    'Revenue(£)': 'sum',
    'Profit(£)': 'sum'
})
regional_summary['Profit_Margin'] = regional_summary['Profit(£)'] / regional_summary['Revenue(£)']

# Create key visualizations
print("Generating visualizations...")

# 1. Distribution plots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

sns.histplot(df_clean['Units Sold'], bins=30, ax=axes[0, 0], kde=True)
axes[0, 0].set_title('Distribution of Units Sold')

sns.histplot(df_clean['Revenue(£)'], bins=30, ax=axes[0, 1], kde=True)
axes[0, 1].set_title('Distribution of Revenue (£)')

sns.histplot(df_clean['Profit(£)'], bins=30, ax=axes[1, 0], kde=True)
axes[1, 0].set_title('Distribution of Profit (£)')

sns.histplot(df_clean['Profit_Margin'], bins=30, ax=axes[1, 1], kde=True)
axes[1, 1].set_title('Distribution of Profit Margin')

plt.tight_layout()
plt.savefig('images/key_distributions.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved key_distributions.png")

# 2. Regional performance
plt.figure(figsize=(10, 6))
sns.barplot(data=regional_summary.sort_values('Profit(£)', ascending=False),
            x='Country(UK)', y='Profit(£)')
plt.title('Total Profit by Region')
plt.ylabel('Profit (£)')
plt.xlabel('Region')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('images/regional_profit.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved regional_profit.png")

# 3. Product performance
conf_summary = df_clean.groupby('Confectionary_clean', as_index=False).agg({
    'Units Sold': 'sum',
    'Revenue(£)': 'sum',
    'Profit(£)': 'sum'
})
conf_summary['Profit_Margin'] = conf_summary['Profit(£)'] / conf_summary['Revenue(£)']

plt.figure(figsize=(10, 6))
sns.barplot(data=conf_summary.sort_values('Profit(£)', ascending=False),
            y='Confectionary_clean', x='Profit(£)')
plt.title('Total Profit by Confectionery Type')
plt.xlabel('Profit (£)')
plt.ylabel('Confectionery Type')
plt.tight_layout()
plt.savefig('images/product_profit.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Saved product_profit.png")

print("\nAll visualizations saved to images/ directory!")
print("You can now add these images to your README.md")
