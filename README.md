# Weather Data Pipeline

A small data pipeline built with Python, pandas and SQLite. It fetches a 7-day weather forecast for several cities from a free API, cleans it, saves it into a database, and summarises it with SQL.

## What it does
1. **Extract:** calls the free Open-Meteo API for each city and reads the 7-day forecast (daily highest and lowest temperature)
2. **Transform:** renames the columns, calculates the average temperature for each day, and adds a `city` column
3. **Load:** stacks the data for all cities into one table and saves it into a SQLite database (`weather.db`, table `daily_weather`)
4. **Check:** runs a SQL query on the database to get each city's average temperature for the week
5. The pipeline writes time-stamped log messages for each step. If one city's request fails, it logs an error for that city and carries on with the rest.

## Example output
The numbers change every day because the forecast changes.

    Saved 21 rows to weather.db
            city  week_avg
    0  Bangalore      24.6
    1    Chennai      28.9
    2  Hyderabad      27.3

21 rows means 7 days for each of 3 cities.

## Project structure
- `Code/weather_pipeline.py`: the pipeline, with one function for each step

No data files are needed, because the data comes straight from the API.

## How to run
1. Install Python, then install the tools with `pip install -r requirements.txt`
2. Make sure you are connected to the internet
3. Open the Code folder and run python weather_pipeline.py from there

The database file `weather.db` is created when the pipeline runs. It isn't included in this repository.

## Adding more cities
Open `weather_pipeline.py`, find the `cities` dictionary in the `main` function, and add a new line with the city's name, latitude and longitude. Nothing else needs to change.

## Tools used
Python, requests, pandas, SQLite, Open-Meteo API

## Author
Vinay Simha M K

Weather data by [Open-Meteo.com](https://open-meteo.com)
