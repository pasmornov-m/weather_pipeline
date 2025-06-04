-- Active: 1747915001397@@127.0.0.1@5432@weather@weather

CREATE DATABASE weather;

-- connect to weather database and run 
CREATE SCHEMA IF NOT EXISTS weather;

CREATE TABLE IF NOT EXISTS weather.fact_openweather_observations (
    observation_id SERIAL PRIMARY KEY,
    country VARCHAR(2),
    city VARCHAR(64),
    timestamp_utc TIMESTAMP NOT NULL,
    temperature NUMERIC(5, 2),
    feels_like NUMERIC(5, 2),
    pressure INTEGER,
    humidity INTEGER,
    weather_main VARCHAR(32),
    weather_description VARCHAR(128),
    wind_speed NUMERIC(5, 2),
    wind_deg INTEGER,
    clouds INTEGER,
    ingestion_time TIMESTAMP DEFAULT NOW()
);
