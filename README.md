# AI's Hidden Cost — Data Centre Resource Intelligence Report

## Overview
Analysis of water, electricity, carbon, and land consumption by AI data centres. Built with Python, SQL, and interactive visualizations.

**Business Question:**
> How much natural resource is consumed and wasted per unit of AI compute — and which companies are doing it most responsibly?

## Key Findings
- ~500ml water evaporated per ~20 ChatGPT queries
- Data centres heading toward 1,000 TWh by 2026 (equal to Japan's grid)
- 37% of electricity never reaches compute hardware — lost to cooling
- 42% of major AI facilities sit in high water-stress zones
- "100% renewable" claims rely on certificates, not physical clean energy

## Project Structure
```
ai-datacenter-resource-analysis/
├── data/                          # Datasets and SQLite database
├── notebooks/                     # Jupyter analysis notebooks (01–05)
├── outputs/                       # Charts, maps, and exports
├── dashboard/                     # Power BI dashboard file
├── generate_data.py               # Synthetic data generator
├── requirements.txt
└── README.md
```

## Setup
```bash
pip install -r requirements.txt
python generate_data.py
jupyter notebook
```

## Data Sources
- IEA Data Centres Report
- Google / Microsoft / Meta / AWS Sustainability Reports
- CDP Carbon Disclosure Project
- WRI Aqueduct (water stress)
- Uptime Institute Annual Reports

## Stack
Python (Pandas, Seaborn, Matplotlib, Folium) · SQL (SQLite) · Power BI / Tableau
