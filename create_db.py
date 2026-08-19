import sqlite3
import os
import pandas as pd

def create_database(csv_path="INDIA_AQI_COMPLETE_20251126.csv", db_path="air_quality.db", include_hourly=False):
    """
    Converts heavy AQI CSV dataset into a lightweight, indexed SQLite database (air_quality.db).
    Storing daily aggregated metrics reduces file size from 282 MB to < 1 MB, enabling seamless GitHub hosting.
    """
    if not os.path.exists(csv_path):
        if os.path.exists(db_path):
            print(f"Database '{db_path}' exists ({os.path.getsize(db_path)/1024:.1f} KB).")
            return
        else:
            raise FileNotFoundError(f"Neither '{csv_path}' nor '{db_path}' was found.")

    print(f"Reading source dataset '{csv_path}'...")
    cols_to_use = [
        'City', 'Datetime', 'US_AQI', 'PM2_5_ugm3', 'Rain_mm', 
        'Wind_Speed_10m_kmh', 'Temp_2m_C', 'Festival_Period', 'Crop_Burning_Season', 'Season'
    ]
    metro_cities = ['Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad', 'Ahmedabad']

    df = pd.read_csv(csv_path, usecols=cols_to_use)
    df_metro = df[df['City'].isin(metro_cities)].copy()

    # Pre-process datetime features
    df_metro['Datetime'] = pd.to_datetime(df_metro['Datetime'])
    df_metro['Date'] = df_metro['Datetime'].dt.date.astype(str)
    df_metro['Month'] = df_metro['Datetime'].dt.to_period('M').dt.to_timestamp().astype(str)
    df_metro['Year'] = df_metro['Datetime'].dt.year

    # Daily aggregation (used by dashboard layout and charts)
    df_daily = df_metro.groupby(['City', 'Date', 'Month', 'Year', 'Season']).agg({
        'US_AQI': 'mean',
        'PM2_5_ugm3': 'mean',
        'Rain_mm': 'sum',
        'Wind_Speed_10m_kmh': 'mean',
        'Temp_2m_C': 'mean',
        'Festival_Period': 'max',
        'Crop_Burning_Season': 'max'
    }).reset_index()

    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    
    # Store daily aggregated dataset (~1 MB)
    df_daily.to_sql('daily_aqi', conn, if_exists='replace', index=False)
    conn.execute('CREATE INDEX idx_daily_city_date ON daily_aqi (City, Date)')

    if include_hourly:
        df_metro['Datetime'] = df_metro['Datetime'].astype(str)
        df_metro.to_sql('city_aqi', conn, if_exists='replace', index=False)
        conn.execute('CREATE INDEX idx_city_datetime ON city_aqi (City, Datetime)')

    conn.commit()
    conn.close()

    db_size_kb = os.path.getsize(db_path) / 1024
    print(f"Successfully generated SQLite database '{db_path}' ({db_size_kb:.1f} KB).")

if __name__ == "__main__":
    create_database()
