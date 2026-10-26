import requests
import pandas as pd 
import sqlite3

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
    df["city"] = city
    return df

def load(df):
    conn = sqlite3.connect("weather.db")
    df.to_sql("daily_weather",conn,if_exists="replace",index=False)
    conn.close()
    print("Saved", len(df), "rows to weather.db")

def check_db():
    conn = sqlite3.connect("weather.db")
    query = """SELECT city, ROUND(AVG(avg_temp), 1) AS week_avg
    FROM daily_weather
    GROUP BY city"""
    print(pd.read_sql(query, conn))
    conn.close()

def main():
    cities = {
        "chennai" : [13.08, 80.27],
        "bangalore" : [12.9716, 77.5946],
        "hyderabad" : [17.38, 78.48]
    }

    all_weather = []
    for city in cities:
        latitude = cities[city][0]
        longitude = cities[city][1]
        raw = extract(latitude, longitude)
        clean = transform(raw, city)
        all_weather.append(clean)

    combined = pd.concat(all_weather)
    load(combined)
    check_db()

main()
