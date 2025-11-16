#!/usr/bin/env python3
"""
Test script to verify data_prep import works
"""

import sys
import os

# Simulate the dashboard import logic
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

print("Testing data_prep import...")
try:
    from data_prep import prepare_data, get_regional_summary
    print("✅ Import successful!")

    # Test data loading
    df = prepare_data("confectionary.xlsx")
    print(f"✅ Data loaded: {len(df)} rows")

    # Test regional summary
    regional = get_regional_summary(df)
    print(f"✅ Regional summary created: {len(regional)} regions")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("🎉 All tests passed!")
