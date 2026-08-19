# Indian Metro Air Quality Dashboard

A high-end, SaaS-quality interactive air quality analytics dashboard for seven major Indian metro cities. This project moves beyond basic Exploratory Data Analysis (EDA) to provide a professional-grade analytical tool with deep insights, dynamic filtering, and a sleek, modern dark-themed user interface.

🚀 **Live Dashboard:** [https://indianairqualitydashboard.streamlit.app/](https://indianairqualitydashboard.streamlit.app/)

---

## 📊 Key Quantitative Insights (Quantized Points)

- **8,470 Daily Records Analyzed**: Multi-year historical dataset spanning from **August 2022 to November 2025** across **7 Indian Metro Cities** (Delhi, Mumbai, Kolkata, Bengaluru, Chennai, Hyderabad, Ahmedabad).
- **Overall Pollution Averages**: Across all cities and years, the overall average PM2.5 level is **38.53 µg/m³** with an average US AQI of **101.52**.
- **Delhi - Highest Pollution Severity**:
  - **70.80 µg/m³** average PM2.5 (highest among all metros).
  - **159.83** average US AQI.
  - **10.08% Severe Days** (US AQI > 200), making Delhi the critical focus area.
- **Secondary Pollution Hotspots**:
  - **Kolkata**: Average PM2.5 of **57.04 µg/m³** (AQI 122.45) with **3.97% Severe Days**.
  - **Mumbai**: Average PM2.5 of **41.41 µg/m³** (AQI 114.22) with **4.05% Severe Days**.
- **Cleaner Metros**:
  - **Bengaluru**: Lowest average PM2.5 at **20.39 µg/m³** (AQI 66.76) and **0.00% Severe Days**.
  - **Chennai**: Average PM2.5 of **22.78 µg/m³** (AQI 74.35) and **0.00% Severe Days**.
  - **Ahmedabad & Hyderabad**: Maintained moderate air quality with **29.94 µg/m³** and **27.37 µg/m³** average PM2.5 respectively, both recording **0.00% Severe Days**.
- **Festival Period Surge (+41.95%)**:
  - Average PM2.5 jumps from **36.90 µg/m³** on normal days to **52.37 µg/m³** during festival periods — representing a **~42% surge** in particulate matter pollution.
- **Meteorological Drivers**:
  - Inverse correlation between wind speed and PM2.5; wind speeds above **15 km/h** demonstrate strong pollutant dispersion across all major urban zones.

---

## Overview

The dashboard analyzes air quality trends, highlights major pollution drivers, and measures the impact of external factors such as weather conditions and festivals on the Air Quality Index (AQI) and PM2.5 levels.

**Included Metro Cities:**
- Delhi
- Mumbai
- Bengaluru
- Chennai
- Kolkata
- Hyderabad
- Ahmedabad

## Features

- **SaaS-Grade UI**: A clean, responsive dark-themed interface built for professional analytics.
- **Dynamic KPI Tracking**: Quick overview of Average PM2.5, Average AQI, Severe Days percentage, and the Most Polluted City based on user-selected filters.
- **Smart Filtering**: Filter data seamlessly by specific cities, years, and seasons.
- **Trend Analysis**: Long-term PM2.5 trends visualized across different cities to spot historical patterns.
- **City Comparison**: Compare average PM2.5 levels and spread (boxplots) across the selected metropolitan areas.
- **Driver Identification**: Analyze how wind speed and major events (like festivals) impact air quality levels.

## Tech Stack

- **Python**: Core programming language.
- **Streamlit & Dash**: Web frameworks for interactive data application delivery.
- **Plotly Express & Graph Objects**: Interactive and high-performance charting.
- **Pandas & NumPy**: Data manipulation, aggregation, and numerical computations.
- **SQLite**: Optimized database storage for rapid query response.

## Project Structure

- `app.py`: Streamlit application script powering the live cloud deployment.
- `dashboard.py`: Analytical Dash application script containing custom layout and interactive callbacks.
- `metro_air_quality_analysis.ipynb`: Jupyter Notebook containing initial exploratory data analysis and insight generation.
- `air_quality.db` & `INDIA_AQI_COMPLETE_20251126.csv`: SQLite database and primary dataset used for analytics.
- Various visual plots (`comparative_boxplot.png`, `correlation_matrix.png`, `seasonal_heatmap.png`, `trend_analysis.png`).

## Setup & Installation

1. **Clone the repository or download the project files.**
2. **Ensure you have Python installed (3.8+ recommended).**
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Ensure the dataset is available:**
   Make sure `air_quality.db` or `INDIA_AQI_COMPLETE_20251126.csv` is present in the project directory.

## Running the Application

### Streamlit App (Live Version)
```bash
streamlit run app.py
```

### Dash App
```bash
python dashboard.py
```

By default, the Streamlit app opens in your browser at `http://localhost:8501`, and the Dash app at `http://127.0.0.1:8050/`.

🌐 **Live URL:** [https://indianairqualitydashboard.streamlit.app/](https://indianairqualitydashboard.streamlit.app/)

## Highlights
- **Automated Insights**: Dynamically highlights critical focus areas (e.g., most polluted city and percentage of severe pollution days based on active filters).
- **Responsive Visualizations**: All charts (trend lines, bar comparisons, donuts, and scatter plots) update instantaneously.

