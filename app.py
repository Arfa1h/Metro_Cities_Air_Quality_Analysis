import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os

# -------------------------------------------------------------
# Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="AQI Analytics SaaS",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# Theme & Custom CSS (SaaS Redesign)
# -------------------------------------------------------------
THEME = {
    'main_bg': '#0B132B',
    'card_bg': '#1C2541',
    'border': '#3A506B',
    'text_primary': '#FFFFFF',
    'text_secondary': '#B0B3C6',
    'cyan': '#00D4FF',
    'purple': '#7B61FF',
    'red': '#FF4C4C',
    'green': '#2ECC71',
    'orange': '#FFA500'
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {{
        background-color: {THEME['main_bg']};
        color: {THEME['text_primary']};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Card Container */
    .kpi-card {{
        background-color: {THEME['card_bg']};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
        margin-bottom: 10px;
    }}
    .kpi-title {{
        font-size: 13px;
        color: {THEME['text_secondary']};
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }}
    .kpi-value {{
        font-size: 32px;
        font-weight: bold;
        color: {THEME['text_primary']};
    }}
    
    /* Insight Banner */
    .insight-box {{
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(123, 97, 255, 0.1) 100%);
        border: 1px solid {THEME['cyan']};
        border-radius: 10px;
        padding: 15px 20px;
        color: {THEME['cyan']};
        font-weight: 500;
        font-size: 15px;
        margin-bottom: 25px;
    }}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Data Loading (SQLite with CSV Fallback)
# -------------------------------------------------------------
DB_PATH = 'air_quality.db'
CSV_PATH = 'INDIA_AQI_COMPLETE_20251126.csv'
DEFAULT_METRO_CITIES = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Ahmedabad']

def get_aqi_category(aqi):
    if aqi <= 50: return 'Good'
    elif aqi <= 100: return 'Moderate'
    elif aqi <= 200: return 'Poor'
    else: return 'Severe'

@st.cache_data
def load_data():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df_daily = pd.read_sql_query("SELECT * FROM daily_aqi", conn)
        conn.close()
        df_daily['Date'] = pd.to_datetime(df_daily['Date']).dt.date
        df_daily['Month'] = pd.to_datetime(df_daily['Month'])
    elif os.path.exists(CSV_PATH):
        from create_db import create_database
        create_database(CSV_PATH, DB_PATH)
        conn = sqlite3.connect(DB_PATH)
        df_daily = pd.read_sql_query("SELECT * FROM daily_aqi", conn)
        conn.close()
        df_daily['Date'] = pd.to_datetime(df_daily['Date']).dt.date
        df_daily['Month'] = pd.to_datetime(df_daily['Month'])
    else:
        st.error("Data file not found. Please ensure air_quality.db is present.")
        return pd.DataFrame()

    df_daily['AQI_Category'] = df_daily['US_AQI'].apply(get_aqi_category)
    return df_daily

df_daily = load_data()

if df_daily.empty:
    st.stop()

available_cities = sorted(df_daily['City'].unique())
available_years = ['All Years'] + sorted(list(df_daily['Year'].unique()))
available_seasons = ['All Seasons'] + sorted(list(df_daily['Season'].dropna().unique()))

# -------------------------------------------------------------
# Sidebar Filters
# -------------------------------------------------------------
st.sidebar.title("🌫️ AQI Analytics")
st.sidebar.markdown("### Filters")

selected_cities = st.sidebar.multiselect(
    "Select Cities",
    options=available_cities,
    default=['Delhi', 'Mumbai', 'Bengaluru'] if set(['Delhi', 'Mumbai', 'Bengaluru']).issubset(set(available_cities)) else available_cities[:3]
)

selected_year = st.sidebar.selectbox("Select Year", options=available_years)
selected_season = st.sidebar.selectbox("Select Season", options=available_seasons)

# Apply Filters
dff = df_daily.copy()

if selected_cities:
    dff = dff[dff['City'].isin(selected_cities)]
else:
    dff = dff[dff['City'].isin(available_cities)]

if selected_year != 'All Years':
    dff = dff[dff['Year'] == selected_year]

if selected_season != 'All Seasons':
    dff = dff[dff['Season'] == selected_season]

# -------------------------------------------------------------
# Helper Plotly Layout
# -------------------------------------------------------------
def get_base_layout(title=""):
    return go.Layout(
        title=dict(text=title, font=dict(color=THEME['text_primary'], size=16)),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=THEME['text_secondary']),
        margin=dict(l=40, r=20, t=50, b=40),
        xaxis=dict(showgrid=False, zeroline=False, color=THEME['text_secondary']),
        yaxis=dict(showgrid=True, gridcolor=THEME['border'], zeroline=False, color=THEME['text_secondary']),
        hovermode="x unified"
    )

# -------------------------------------------------------------
# Main Dashboard UI
# -------------------------------------------------------------
st.title("Indian Metro Air Quality Analytics")
st.markdown("Interactive analysis of AQI, PM2.5 trends, weather correlations, and seasonal drivers.")

if dff.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# Insights calculation
city_summary = dff.groupby('City')['PM2_5_ugm3'].mean().reset_index()
most_polluted = city_summary.sort_values(by='PM2_5_ugm3', ascending=False).iloc[0]['City'] if not city_summary.empty else 'N/A'
most_polluted_val = city_summary.sort_values(by='PM2_5_ugm3', ascending=False).iloc[0]['PM2_5_ugm3'] if not city_summary.empty else 0
severe_pct = (len(dff[dff['AQI_Category'] == 'Severe']) / len(dff) * 100) if len(dff) > 0 else 0

st.markdown(
    f'<div class="insight-box">💡 <b>Insight:</b> {most_polluted} represents the critical focus area with an average PM2.5 of {most_polluted_val:.1f} µg/m³. {severe_pct:.1f}% of recorded days were classified as severe.</div>',
    unsafe_allow_html=True
)

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_pm = dff['PM2_5_ugm3'].mean()
    st.markdown(f'''
    <div class="kpi-card" style="border-left: 4px solid {THEME['cyan']};">
        <div class="kpi-title">AVG PM2.5</div>
        <div class="kpi-value">{avg_pm:.1f}</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    avg_aqi = dff['US_AQI'].mean()
    st.markdown(f'''
    <div class="kpi-card" style="border-left: 4px solid {THEME['purple']};">
        <div class="kpi-title">AVG AQI</div>
        <div class="kpi-value">{avg_aqi:.0f}</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="kpi-card" style="border-left: 4px solid {THEME['green']};">
        <div class="kpi-title">SEVERE DAYS</div>
        <div class="kpi-value">{severe_pct:.1f}%</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    st.markdown(f'''
    <div class="kpi-card" style="border-left: 4px solid {THEME['red']};">
        <div class="kpi-title">MOST POLLUTED</div>
        <div class="kpi-value">{most_polluted}</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# Chart 1: PM2.5 Long-Term Trend
# -------------------------------------------------------------
trend_df = dff.groupby(['Month', 'City'])['PM2_5_ugm3'].mean().reset_index()
fig_main = go.Figure(layout=get_base_layout("PM2.5 Long-Term Trend"))

colors = [THEME['cyan'], THEME['purple'], THEME['red'], THEME['green'], THEME['orange'], '#E0C3FC', '#8EC5FC']
for i, city in enumerate(trend_df['City'].unique()):
    city_data = trend_df[trend_df['City'] == city]
    fig_main.add_trace(go.Scatter(
        x=city_data['Month'], y=city_data['PM2_5_ugm3'],
        mode='lines', name=city,
        line=dict(color=colors[i % len(colors)], width=2.5)
    ))

st.plotly_chart(fig_main, use_container_width=True)

# -------------------------------------------------------------
# Row 2: City Comparison & Boxplot
# -------------------------------------------------------------
r2_col1, r2_col2 = st.columns(2)

with r2_col1:
    fig_comp = go.Figure(data=[go.Bar(
        x=city_summary['City'], y=city_summary['PM2_5_ugm3'],
        marker_color=[THEME['red'] if c == most_polluted else THEME['border'] for c in city_summary['City']]
    )], layout=get_base_layout("City Comparison (Avg PM2.5)"))
    st.plotly_chart(fig_comp, use_container_width=True)

with r2_col2:
    fig_box = go.Figure(layout=get_base_layout("PM2.5 Distribution (Boxplot)"))
    for i, city in enumerate(dff['City'].unique()):
        fig_box.add_trace(go.Box(
            y=dff[dff['City'] == city]['PM2_5_ugm3'], name=city,
            marker_color=colors[i % len(colors)], boxpoints=False
        ))
    fig_box.update_layout(showlegend=False)
    st.plotly_chart(fig_box, use_container_width=True)

# -------------------------------------------------------------
# Row 3: Donut, Event Impact, Drivers Scatter
# -------------------------------------------------------------
r3_col1, r3_col2, r3_col3 = st.columns(3)

with r3_col1:
    cat_counts = dff['AQI_Category'].value_counts()
    color_map = {'Good': THEME['green'], 'Moderate': THEME['cyan'], 'Poor': THEME['orange'], 'Severe': THEME['red']}
    pie_colors = [color_map.get(c, THEME['border']) for c in cat_counts.index]
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=cat_counts.index, values=cat_counts.values,
        hole=0.6, marker_colors=pie_colors,
        textinfo='percent', hoverinfo='label+value'
    )], layout=get_base_layout("AQI Category Share"))
    fig_donut.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig_donut, use_container_width=True)

with r3_col2:
    event_df = dff.groupby('Festival_Period')['PM2_5_ugm3'].mean().reset_index()
    event_df['Period'] = event_df['Festival_Period'].map({0: 'Normal Days', 1: 'Festival Days'})
    fig_event = go.Figure(data=[go.Bar(
        x=event_df['Period'], y=event_df['PM2_5_ugm3'],
        marker_color=[THEME['border'], THEME['purple']], width=0.4
    )], layout=get_base_layout("Festival Impact on PM2.5"))
    st.plotly_chart(fig_event, use_container_width=True)

with r3_col3:
    median_pm25 = dff['PM2_5_ugm3'].median()
    fig_scatter = go.Figure(layout=get_base_layout("Wind vs PM2.5 Correlation"))
    fig_scatter.add_trace(go.Scatter(
        x=dff['Wind_Speed_10m_kmh'], y=dff['PM2_5_ugm3'],
        mode='markers', marker=dict(color=THEME['cyan'], opacity=0.3, size=6),
        hovertemplate="Wind: %{x:.1f} km/h<br>PM2.5: %{y:.1f}<extra></extra>"
    ))
    fig_scatter.add_hline(y=median_pm25, line_dash="dash", line_color=THEME['red'], annotation_text="Median PM2.5")
    fig_scatter.update_layout(xaxis_title="Wind Speed (km/h)")
    st.plotly_chart(fig_scatter, use_container_width=True)
