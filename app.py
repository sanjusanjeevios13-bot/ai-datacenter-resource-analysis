"""
Interactive Plotly Dash Dashboard — AI Data Centre Resource Intelligence Report
Run: python app.py
Open: http://127.0.0.1:8050
"""

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.read_csv('data/ai_datacenter_enriched.csv')
locations = pd.read_csv('data/datacenter_locations.csv')

company_df = df[df['company'] != 'All'].copy()
global_df = df[df['company'] == 'All'].copy()

COLORS = {
    'Google': '#4285F4', 'Microsoft': '#00A4EF',
    'Meta': '#0668E1', 'AWS': '#FF9900', 'All': '#888888'
}
BG = '#0f1117'
CARD_BG = '#1a1d29'
TEXT = '#e0e0e0'

app = dash.Dash(__name__)
app.title = "AI Data Centre Resource Intelligence"

def kpi_card(title, value, subtitle=""):
    return html.Div([
        html.P(title, style={'margin': '0', 'fontSize': '12px', 'color': '#888', 'textTransform': 'uppercase'}),
        html.H2(value, style={'margin': '5px 0', 'color': '#00e676', 'fontSize': '28px'}),
        html.P(subtitle, style={'margin': '0', 'fontSize': '11px', 'color': '#666'}),
    ], style={
        'backgroundColor': CARD_BG, 'padding': '20px', 'borderRadius': '10px',
        'textAlign': 'center', 'flex': '1', 'margin': '0 8px',
    })

latest = company_df[company_df['year'] == company_df['year'].max()]
latest_global = global_df[global_df['year'] == global_df['year'].max()]

app.layout = html.Div(style={'backgroundColor': BG, 'minHeight': '100vh', 'padding': '20px', 'fontFamily': 'Arial'}, children=[

    html.H1("AI's Hidden Cost: Data Centre Resource Intelligence Report",
            style={'color': TEXT, 'textAlign': 'center', 'marginBottom': '5px'}),
    html.P("How much water, electricity, and carbon does AI actually consume?",
           style={'color': '#888', 'textAlign': 'center', 'marginBottom': '25px'}),

    # KPI Cards
    html.Div(style={'display': 'flex', 'marginBottom': '25px'}, children=[
        kpi_card("Global DC Energy", f"{latest_global['electricity_gwh'].values[0]/1000:.0f} TWh", "2024 estimate"),
        kpi_card("Avg Industry PUE", f"{latest_global['pue'].values[0]:.2f}", "1.0 = perfect efficiency"),
        kpi_card("Avg Renewable Gap", f"{latest['renewable_gap_pct'].mean():.0f}%", "Pledged minus actual"),
        kpi_card("High Stress DCs", f"{(locations['wri_stress_score'] >= 3).sum()}/{len(locations)}",
                 f"{(locations['wri_stress_score'] >= 3).mean()*100:.0f}% in stressed zones"),
    ]),

    # Slicers
    html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '20px'}, children=[
        html.Div([
            html.Label("Company", style={'color': TEXT, 'fontSize': '12px'}),
            dcc.Dropdown(
                id='company-filter',
                options=[{'label': c, 'value': c} for c in ['All'] + sorted(company_df['company'].unique())],
                value='All', clearable=False,
                style={'backgroundColor': CARD_BG, 'color': '#000'}
            ),
        ], style={'flex': '1'}),
        html.Div([
            html.Label("Year Range", style={'color': TEXT, 'fontSize': '12px'}),
            dcc.RangeSlider(
                id='year-slider',
                min=df['year'].min(), max=df['year'].max(),
                value=[df['year'].min(), df['year'].max()],
                marks={y: str(y) for y in range(df['year'].min(), df['year'].max()+1, 2)},
                step=1,
            ),
        ], style={'flex': '3'}),
    ]),

    # Row 1: Energy Projection + PUE Trends
    html.Div(style={'display': 'flex', 'gap': '15px', 'marginBottom': '15px'}, children=[
        html.Div([dcc.Graph(id='energy-projection')], style={'flex': '1', 'backgroundColor': CARD_BG, 'borderRadius': '10px', 'padding': '10px'}),
        html.Div([dcc.Graph(id='pue-trends')], style={'flex': '1', 'backgroundColor': CARD_BG, 'borderRadius': '10px', 'padding': '10px'}),
    ]),

    # Row 2: Map + Energy Waste
    html.Div(style={'display': 'flex', 'gap': '15px', 'marginBottom': '15px'}, children=[
        html.Div([dcc.Graph(id='dc-map')], style={'flex': '1', 'backgroundColor': CARD_BG, 'borderRadius': '10px', 'padding': '10px'}),
        html.Div([dcc.Graph(id='energy-waste')], style={'flex': '1', 'backgroundColor': CARD_BG, 'borderRadius': '10px', 'padding': '10px'}),
    ]),

    # Row 3: Renewable Gap + CO2
    html.Div(style={'display': 'flex', 'gap': '15px', 'marginBottom': '15px'}, children=[
        html.Div([dcc.Graph(id='renewable-gap')], style={'flex': '1', 'backgroundColor': CARD_BG, 'borderRadius': '10px', 'padding': '10px'}),
        html.Div([dcc.Graph(id='co2-trends')], style={'flex': '1', 'backgroundColor': CARD_BG, 'borderRadius': '10px', 'padding': '10px'}),
    ]),

    # Row 4: WUE Bar + Scatter
    html.Div(style={'display': 'flex', 'gap': '15px', 'marginBottom': '15px'}, children=[
        html.Div([dcc.Graph(id='wue-bar')], style={'flex': '1', 'backgroundColor': CARD_BG, 'borderRadius': '10px', 'padding': '10px'}),
        html.Div([dcc.Graph(id='scatter-cap')], style={'flex': '1', 'backgroundColor': CARD_BG, 'borderRadius': '10px', 'padding': '10px'}),
    ]),

    html.P("Data sources: IEA, Google/Microsoft/Meta/AWS Sustainability Reports, WRI Aqueduct, Uptime Institute | Synthetic data for portfolio demonstration",
           style={'color': '#555', 'textAlign': 'center', 'fontSize': '11px', 'marginTop': '20px'}),
])


def filter_data(company, year_range):
    filtered = company_df[(company_df['year'] >= year_range[0]) & (company_df['year'] <= year_range[1])]
    if company != 'All':
        filtered = filtered[filtered['company'] == company]
    return filtered


@app.callback(
    [Output('energy-projection', 'figure'),
     Output('pue-trends', 'figure'),
     Output('dc-map', 'figure'),
     Output('energy-waste', 'figure'),
     Output('renewable-gap', 'figure'),
     Output('co2-trends', 'figure'),
     Output('wue-bar', 'figure'),
     Output('scatter-cap', 'figure')],
    [Input('company-filter', 'value'),
     Input('year-slider', 'value')]
)
def update_charts(company, year_range):
    filtered = filter_data(company, year_range)
    template = 'plotly_dark'

    # 1. Energy Projection
    gd = global_df.sort_values('year')
    x, y = gd['year'].values, gd['electricity_gwh'].values
    coeffs = np.polyfit(x, y, 2)
    poly = np.poly1d(coeffs)
    future = np.arange(2015, 2031)
    bau = poly(future)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=x, y=y/1000, mode='lines+markers', name='Actual', line=dict(color='#00e676', width=3)))
    mask = future > x.max()
    fig1.add_trace(go.Scatter(x=future[mask], y=bau[mask]/1000, mode='lines', name='BAU', line=dict(color='#ff5252', width=2, dash='dash')))
    fig1.add_trace(go.Scatter(x=future[mask], y=bau[mask]*0.85/1000, mode='lines', name='Efficiency -15%', line=dict(color='#ffc400', width=2, dash='dash')))
    fig1.add_hline(y=1000, line_dash="dot", line_color="white", opacity=0.3, annotation_text="Japan's grid")
    fig1.update_layout(template=template, title='Global DC Energy → 2030 (TWh)', paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=350, margin=dict(t=40, b=30))

    # 2. PUE Trends
    fig2 = go.Figure()
    companies_to_plot = [company] if company != 'All' else ['Google', 'Microsoft', 'Meta', 'AWS']
    for c in companies_to_plot:
        sub = filtered[filtered['company'] == c].sort_values('year')
        fig2.add_trace(go.Scatter(x=sub['year'], y=sub['pue'], mode='lines+markers', name=c, line=dict(color=COLORS[c], width=2.5)))
    fig2.add_hline(y=1.58, line_dash="dash", line_color="#ff5252", annotation_text="Industry Avg")
    fig2.add_hline(y=1.2, line_dash="dash", line_color="#00e676", annotation_text="Excellent")
    fig2.update_layout(template=template, title='PUE Over Time', paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=350, margin=dict(t=40, b=30))

    # 3. Map
    loc = locations.copy()
    if company != 'All':
        loc = loc[loc['company'] == company]
    loc['color'] = loc['wri_stress_score'].apply(lambda s: 'red' if s >= 3 else 'orange' if s >= 2 else 'green')
    loc['stress_label'] = loc['wri_stress_score'].apply(lambda s: 'High' if s >= 3 else 'Medium' if s >= 2 else 'Low')
    fig3 = px.scatter_geo(loc, lat='lat', lon='lon', size='capacity_mw', color='stress_label',
                          color_discrete_map={'High': '#ff5252', 'Medium': '#ffc400', 'Low': '#00e676'},
                          hover_name='name', hover_data=['company', 'capacity_mw', 'wri_stress_score'],
                          size_max=25, projection='natural earth')
    fig3.update_layout(template=template, title='Data Centres & Water Stress', paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
                       geo=dict(bgcolor=CARD_BG, landcolor='#2a2d3a', oceancolor='#0f1117', showocean=True),
                       height=350, margin=dict(t=40, b=10))

    # 4. Energy Waste Bars
    latest_f = filtered[filtered['year'] == filtered['year'].max()].sort_values('energy_waste_pct')
    fig4 = go.Figure(go.Bar(
        y=latest_f['company'], x=latest_f['energy_waste_pct'], orientation='h',
        marker_color=[COLORS.get(c, '#888') for c in latest_f['company']],
        text=[f"{v:.1f}%" for v in latest_f['energy_waste_pct']], textposition='outside'
    ))
    fig4.add_vline(x=36.7, line_dash="dash", line_color="#ff5252", annotation_text="Ind. Avg")
    fig4.update_layout(template=template, title='Energy Waste % (Latest Year)', paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=350, margin=dict(t=40, b=30))

    # 5. Renewable Gap
    fig5 = go.Figure()
    for c in companies_to_plot:
        sub = filtered[filtered['company'] == c].sort_values('year')
        fig5.add_trace(go.Scatter(x=sub['year'], y=sub['renewable_pledged_pct'], mode='lines', name=f'{c} Pledged', line=dict(color=COLORS[c], width=1.5, dash='dash')))
        fig5.add_trace(go.Scatter(x=sub['year'], y=sub['renewable_actual_pct'], mode='lines+markers', name=f'{c} Actual', line=dict(color=COLORS[c], width=2.5)))
    fig5.update_layout(template=template, title='Renewable Energy: Pledge vs Actual %', paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=350, margin=dict(t=40, b=30))

    # 6. CO2 Trends
    fig6 = go.Figure()
    for c in companies_to_plot:
        sub = filtered[filtered['company'] == c].sort_values('year')
        fig6.add_trace(go.Scatter(x=sub['year'], y=sub['co2_tons']/1e6, mode='lines+markers', name=c,
                                  line=dict(color=COLORS[c], width=2.5), fill='tozeroy'))
    fig6.update_layout(template=template, title='CO₂ Emissions (Million Tonnes)', paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=350, margin=dict(t=40, b=30))

    # 7. WUE Bar
    wue_data = filtered.groupby('company')['wue'].mean().sort_values().reset_index()
    fig7 = go.Figure(go.Bar(
        x=wue_data['company'], y=wue_data['wue'],
        marker_color=[COLORS.get(c, '#888') for c in wue_data['company']],
        text=[f"{v:.2f}" for v in wue_data['wue']], textposition='outside'
    ))
    fig7.update_layout(template=template, title='Avg Water Usage Effectiveness (WUE)', paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=350, margin=dict(t=40, b=30))

    # 8. Scatter: Capacity vs PUE
    fig8 = px.scatter(filtered, x='electricity_gwh', y='pue', color='company', size='water_litres',
                      color_discrete_map=COLORS, hover_data=['year', 'energy_waste_pct'],
                      size_max=30)
    fig8.add_hline(y=1.58, line_dash="dash", line_color="#ff5252", annotation_text="Ind. Avg")
    fig8.update_layout(template=template, title='Capacity vs Efficiency (bubble=water)', paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, height=350, margin=dict(t=40, b=30))

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8


if __name__ == '__main__':
    print("Starting dashboard at http://127.0.0.1:8050")
    app.run(debug=True, port=8050)
