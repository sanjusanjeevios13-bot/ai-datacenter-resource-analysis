"""
Export a single denormalized CSV optimized for Power BI / Tableau import.
All metrics, derived columns, and location data merged into one flat table.
"""

import pandas as pd
import numpy as np

df = pd.read_csv('data/ai_datacenter_enriched.csv')
locations = pd.read_csv('data/datacenter_locations.csv')

loc_summary = locations.groupby('company').agg(
    total_capacity_mw=('capacity_mw', 'sum'),
    avg_stress_score=('wri_stress_score', 'mean'),
    max_stress_score=('wri_stress_score', 'max'),
    high_stress_count=('wri_stress_score', lambda x: (x >= 3).sum()),
    location_count=('name', 'count'),
).reset_index()

merged = df.merge(loc_summary, on='company', how='left')

merged['pue_tier'] = pd.cut(merged['pue'],
    bins=[0, 1.2, 1.4, 1.6, 3.0],
    labels=['Excellent', 'Good', 'Average', 'Poor'])

merged['renewable_status'] = merged['renewable_gap_pct'].apply(
    lambda x: 'High Greenwash Risk' if x > 20
    else 'Moderate Gap' if x > 10
    else 'On Track' if pd.notna(x) else None)

merged['energy_waste_tier'] = pd.cut(merged['energy_waste_pct'],
    bins=[0, 15, 25, 35, 100],
    labels=['Excellent', 'Good', 'Average', 'Poor'])

merged['water_billion_litres'] = merged['water_litres'] / 1e9
merged['electricity_twh'] = merged['electricity_gwh'] / 1000
merged['co2_million_tonnes'] = merged['co2_tons'] / 1e6

merged.to_csv('data/powerbi_ready.csv', index=False)
print(f"Exported: data/powerbi_ready.csv ({merged.shape[0]} rows, {merged.shape[1]} columns)")
print(f"\nColumns:\n{list(merged.columns)}")
