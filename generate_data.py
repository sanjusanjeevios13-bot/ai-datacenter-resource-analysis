"""
Generate realistic synthetic datasets for AI Data Centre Resource Analysis.
Based on publicly reported figures from Google, Microsoft, Meta, AWS sustainability reports,
IEA projections, and Uptime Institute benchmarks.
"""

import pandas as pd
import numpy as np
import os

np.random.seed(42)

YEARS = list(range(2015, 2025))
COMPANIES = ['Google', 'Microsoft', 'Meta', 'AWS']


def generate_master_data():
    rows = []

    baselines = {
        'Google': {
            'electricity_2015': 7.7, 'electricity_growth': 1.14,
            'pue_start': 1.12, 'pue_end': 1.10,
            'water_factor': 1.8e9, 'water_growth': 1.12,
            'renewable_pledged': [37, 44, 56, 67, 73, 80, 90, 100, 100, 100],
            'renewable_actual':  [34, 40, 50, 58, 61, 67, 76, 82, 85, 90],
            'co2_start': 2.9e6, 'co2_reduction': 0.94,
            'queries_start': 800, 'queries_growth': 1.18,
            'facilities': [15, 17, 19, 21, 23, 24, 27, 30, 33, 36],
        },
        'Microsoft': {
            'electricity_2015': 5.5, 'electricity_growth': 1.16,
            'pue_start': 1.22, 'pue_end': 1.12,
            'water_factor': 2.5e9, 'water_growth': 1.15,
            'renewable_pledged': [30, 40, 50, 60, 70, 80, 100, 100, 100, 100],
            'renewable_actual':  [25, 32, 40, 48, 53, 60, 68, 72, 78, 83],
            'co2_start': 3.8e6, 'co2_reduction': 0.95,
            'queries_start': 200, 'queries_growth': 1.25,
            'facilities': [20, 24, 30, 36, 42, 50, 58, 60, 65, 70],
        },
        'Meta': {
            'electricity_2015': 2.5, 'electricity_growth': 1.20,
            'pue_start': 1.25, 'pue_end': 1.10,
            'water_factor': 1.2e9, 'water_growth': 1.18,
            'renewable_pledged': [25, 35, 51, 75, 86, 100, 100, 100, 100, 100],
            'renewable_actual':  [20, 28, 43, 58, 65, 75, 80, 86, 90, 94],
            'co2_start': 1.5e6, 'co2_reduction': 0.93,
            'queries_start': 50, 'queries_growth': 1.35,
            'facilities': [6, 7, 8, 10, 12, 15, 18, 20, 22, 24],
        },
        'AWS': {
            'electricity_2015': 8.0, 'electricity_growth': 1.18,
            'pue_start': 1.30, 'pue_end': 1.15,
            'water_factor': 3.0e9, 'water_growth': 1.16,
            'renewable_pledged': [25, 30, 40, 50, 65, 76, 85, 100, 100, 100],
            'renewable_actual':  [18, 22, 30, 38, 45, 50, 56, 62, 68, 75],
            'co2_start': 5.2e6, 'co2_reduction': 0.96,
            'queries_start': 500, 'queries_growth': 1.22,
            'facilities': [30, 35, 42, 50, 60, 70, 80, 84, 90, 100],
        },
    }

    regions = ['North America', 'Europe', 'Asia-Pacific']

    for company, b in baselines.items():
        pue_values = np.linspace(b['pue_start'], b['pue_end'], len(YEARS))

        for i, year in enumerate(YEARS):
            electricity = b['electricity_2015'] * (b['electricity_growth'] ** i)
            electricity += np.random.normal(0, electricity * 0.03)

            pue = pue_values[i] + np.random.normal(0, 0.01)
            pue = max(1.05, pue)
            it_load = electricity / pue

            water = b['water_factor'] * (b['water_growth'] ** i)
            water += np.random.normal(0, water * 0.05)
            water_consumed = water * np.random.uniform(0.55, 0.75)

            wue = water / (it_load * 1e6)

            co2 = b['co2_start'] * (b['co2_reduction'] ** i)
            co2 += np.random.normal(0, co2 * 0.04)

            cue = co2 / (electricity * 1e3)

            queries = b['queries_start'] * (b['queries_growth'] ** i)
            queries += np.random.normal(0, queries * 0.05)

            rows.append({
                'company': company,
                'year': year,
                'electricity_gwh': round(electricity, 2),
                'it_load_gwh': round(it_load, 2),
                'water_litres': round(water),
                'water_consumed_litres': round(water_consumed),
                'pue': round(pue, 3),
                'wue': round(wue, 3),
                'cue': round(cue, 4),
                'co2_tons': round(co2),
                'renewable_pledged_pct': b['renewable_pledged'][i],
                'renewable_actual_pct': b['renewable_actual'][i],
                'queries_million': round(queries, 1),
                'region': np.random.choice(regions, p=[0.5, 0.3, 0.2]),
                'facility_count': b['facilities'][i],
            })

    global_energy_twh = [
        400, 415, 430, 450, 475, 500, 540, 600, 700, 850
    ]
    for i, year in enumerate(YEARS):
        rows.append({
            'company': 'All',
            'year': year,
            'electricity_gwh': global_energy_twh[i] * 1000,
            'it_load_gwh': round(global_energy_twh[i] * 1000 / 1.58, 2),
            'water_litres': round(global_energy_twh[i] * 1e9 * 4.2),
            'water_consumed_litres': round(global_energy_twh[i] * 1e9 * 2.8),
            'pue': round(1.58 - (i * 0.01) + np.random.normal(0, 0.005), 3),
            'wue': round(1.8 - (i * 0.02) + np.random.normal(0, 0.02), 3),
            'cue': round(0.45 - (i * 0.008) + np.random.normal(0, 0.005), 4),
            'co2_tons': round(global_energy_twh[i] * 1e3 * 0.42),
            'renewable_pledged_pct': round(20 + i * 4.5),
            'renewable_actual_pct': round(15 + i * 3.2),
            'queries_million': round(5000 * (1.3 ** i), 1),
            'region': 'Global',
            'facility_count': round(8000 + i * 500),
        })

    df = pd.DataFrame(rows)
    return df


def generate_location_data():
    locations = [
        ('The Dalles', 'Google', 45.5946, -121.1787, 200, 1.5),
        ('Council Bluffs', 'Google', 41.2619, -95.8608, 350, 2.0),
        ('Lenoir', 'Google', 35.9140, -81.5390, 150, 1.2),
        ('Mayes County', 'Google', 36.3000, -95.2000, 250, 2.8),
        ('Hamina', 'Google', 60.5693, 27.1878, 120, 0.8),
        ('St. Ghislain', 'Google', 50.4490, 3.8190, 180, 1.5),
        ('Changhua', 'Google', 24.0518, 120.5161, 100, 3.5),
        ('Singapore', 'Google', 1.3521, 103.8198, 80, 4.2),

        ('Quincy', 'Microsoft', 47.2343, -119.8526, 400, 2.5),
        ('San Antonio', 'Microsoft', 29.4241, -98.4936, 300, 4.0),
        ('Des Moines', 'Microsoft', 41.5868, -93.6250, 250, 2.2),
        ('Cheyenne', 'Microsoft', 41.1400, -104.8202, 200, 3.2),
        ('Dublin', 'Microsoft', 53.3498, -6.2603, 180, 1.0),
        ('Amsterdam', 'Microsoft', 52.3676, 4.9041, 220, 1.3),
        ('Pune', 'Microsoft', 18.5204, 73.8567, 120, 4.5),
        ('Phoenix', 'Microsoft', 33.4484, -112.0740, 350, 4.8),

        ('Prineville', 'Meta', 44.3101, -120.8340, 280, 2.0),
        ('Forest City', 'Meta', 35.3340, -81.8651, 180, 1.5),
        ('Fort Worth', 'Meta', 32.7555, -97.3308, 350, 3.8),
        ('Lulea', 'Meta', 65.5848, 22.1547, 200, 0.5),
        ('Clonee', 'Meta', 53.4169, -6.6842, 220, 1.0),
        ('Singapore DC', 'Meta', 1.2930, 103.8558, 150, 4.2),
        ('Mesa', 'Meta', 33.4152, -111.8315, 300, 4.5),

        ('Ashburn', 'AWS', 39.0438, -77.4874, 600, 2.0),
        ('Columbus', 'AWS', 39.9612, -82.9988, 250, 1.8),
        ('Oregon', 'AWS', 44.0521, -123.0868, 400, 1.5),
        ('Mumbai', 'AWS', 19.0760, 72.8777, 200, 4.8),
        ('Sao Paulo', 'AWS', -23.5505, -46.6333, 150, 3.0),
        ('Frankfurt', 'AWS', 50.1109, 8.6821, 300, 1.2),
        ('Cape Town', 'AWS', -33.9249, 18.4241, 100, 3.8),
        ('Bahrain', 'AWS', 26.0667, 50.5577, 180, 5.0),
        ('Stockholm', 'AWS', 59.3293, 18.0686, 200, 0.8),
        ('Tokyo', 'AWS', 35.6762, 139.6503, 250, 2.5),
    ]

    df = pd.DataFrame(locations, columns=[
        'name', 'company', 'lat', 'lon', 'capacity_mw', 'wri_stress_score'
    ])
    return df


if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)

    master = generate_master_data()
    master.to_csv('data/ai_datacenter_master.csv', index=False)
    print(f"Master dataset: {master.shape[0]} rows, {master.shape[1]} columns")
    print(master.head())

    locations = generate_location_data()
    locations.to_csv('data/datacenter_locations.csv', index=False)
    print(f"\nLocations dataset: {locations.shape[0]} data centres")
    print(locations.head())

    print("\nData generation complete.")
