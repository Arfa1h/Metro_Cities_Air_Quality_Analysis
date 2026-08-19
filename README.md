# Indian Metro Air Quality Dashboard

A high-end, SaaS-quality interactive air quality analytics dashboard for seven major Indian metro cities. This project moves beyond basic Exploratory Data Analysis (EDA) to provide a professional-grade analytical tool with deep insights, dynamic filtering, and a sleek, modern dark-themed user interface.

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
- **Dash**: Web framework for building the analytical web application.
- **Plotly Express & Graph Objects**: Interactive and high-performance charting.
- **Pandas**: Data manipulation and aggregation.
- **NumPy**: Numerical operations.

## Project Structure

- `dashboard.py`: The main Dash application script containing the layout, styling, data aggregation, and interactive callbacks.
- `metro_air_quality_analysis.ipynb`: A Jupyter Notebook containing initial exploratory data analysis and insight generation.
- `INDIA_AQI_COMPLETE_20251126.csv`: The primary dataset used for the dashboard's analytics.
- Various image files (`comparative_boxplot.png`, `correlation_matrix.png`, `seasonal_heatmap.png`, `trend_analysis.png`) representing static plots generated during the EDA phase.

## Setup & Installation

1. **Clone the repository or download the project files.**
2. **Ensure you have Python installed (3.8+ recommended).**
3. **Install the required dependencies:**
   ```bash
   pip install dash plotly pandas numpy
   ```
4. **Ensure the dataset is available:**
   Make sure `INDIA_AQI_COMPLETE_20251126.csv` is present in the same directory as `dashboard.py`.

## Running the Application

To start the dashboard locally, run the following command in your terminal:

```bash
python dashboard.py
```

By default, the Dash application will be available at `http://127.0.0.1:8050/`. Open this URL in your web browser to view the interactive dashboard.

## Highlights
- **Insight Box**: An automated insight generator that immediately highlights critical areas of concern (e.g., the most polluted city and the percentage of severe days in the selected parameters).
- **Responsive Charts**: All charts (trend lines, bar comparisons, donuts, and scatters) update instantaneously as you interact with the filters in the header.
