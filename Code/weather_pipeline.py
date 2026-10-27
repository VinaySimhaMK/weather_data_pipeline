import requests
import pandas as pd 
import sqlite3
import logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S"
)

def extract(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params  = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "Asia/Kolkata",
        "forecast_days": 7,
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    return pd.DataFrame(data["daily"])

def transform(df, city):
    df = df.rename(columns={
        "time" : "date",
        "temperature_2m_max" : "max_temp",
        "temperature_2m_min" : "min_temp"
    })
    df["avg_temp"] = ((df["max_temp"] + df["min_temp"])/2).round(1)
    df["city"] = city.title()
    return df

def load(df):
    conn = sqlite3.connect("weather.db")
    try:
        old = pd.read_sql("SELECT * FROM daily_weather", conn)
        df = pd.concat([old, df])
    except Exception:
        logging.info("No old data found, starting a new table")
    df = df.drop_duplicates(subset=["date", "city"], keep="last")
    df.to_sql("daily_weather", conn, if_exists="replace", index=False)
    conn.close()
    logging.info("Table now holds %d rows", len(df))

def check_db():
    conn = sqlite3.connect("weather.db")
    query = """SELECT city, ROUND(AVG(avg_temp), 1) AS week_avg
    FROM daily_weather
    GROUP BY city"""
    print(pd.read_sql(query, conn))
    count = pd.read_sql("SELECT COUNT(*) AS rows_in_table FROM daily_weather", conn)
    print(count)
    conn.close()

def main():
    cities = {
        "chennai" : [13.08, 80.27],
        "bangalore" : [12.9716, 77.5946],
        "hyderabad" : [17.38, 78.48]
    }

    all_weather = []
    for city in cities:
        logging.info("Extracting weather for %s", city.title())
        try:
            latitude = cities[city][0]
            longitude = cities[city][1]
            raw = extract(latitude, longitude)
            clean = transform(raw, city)
            all_weather.append(clean)
        except Exception as error:
            logging.error("Could not get weather for %s: %s", city.title(), error)

    if len(all_weather) == 0:
        logging.error("No data was collected, nothing to save")
        return
        
    combined = pd.concat(all_weather)
    load(combined)
    check_db()

main()