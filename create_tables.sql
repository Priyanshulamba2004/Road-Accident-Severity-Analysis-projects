-- Road Accident Severity Analysis - SQL Schema & Indexes

-- CREATE DATABASE road_accident_db;
-- USE road_accident_db;

DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS accidents;
DROP TABLE IF EXISTS weather_stations;

CREATE TABLE IF NOT EXISTS weather_stations (
    station_id      VARCHAR(50) PRIMARY KEY,
    station_name    VARCHAR(100),
    city            VARCHAR(100),
    state           VARCHAR(100),
    avg_rainfall    NUMERIC(10, 2),
    avg_visibility  NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS accidents (
    accident_id        VARCHAR(50) PRIMARY KEY,
    accident_date      DATE,
    accident_time      TIME,
    latitude           NUMERIC(9, 6),
    longitude          NUMERIC(9, 6),
    severity           INT,
    weather            VARCHAR(50),
    light_conditions   VARCHAR(50),
    road_type          VARCHAR(50),
    city               VARCHAR(100),
    state              VARCHAR(100),
    station_id         VARCHAR(50),
    CONSTRAINT fk_accidents_weather
        FOREIGN KEY (station_id) REFERENCES weather_stations(station_id)
);

CREATE TABLE IF NOT EXISTS vehicles (
    accident_id    VARCHAR(50),
    vehicle_id     VARCHAR(50),
    vehicle_type   VARCHAR(50),
    age_of_driver  INT,
    PRIMARY KEY (accident_id, vehicle_id),
    CONSTRAINT fk_vehicles_accidents
        FOREIGN KEY (accident_id) REFERENCES accidents(accident_id)
);

CREATE INDEX idx_accidents_severity
    ON accidents (severity);

CREATE INDEX idx_accidents_city_state
    ON accidents (city, state);

CREATE INDEX idx_accidents_datetime
    ON accidents (accident_date, accident_time);

CREATE INDEX idx_accidents_lat_long
    ON accidents (latitude, longitude);

CREATE INDEX idx_vehicles_vehicletype
    ON vehicles (vehicle_type);

CREATE OR REPLACE VIEW vw_accidents_by_severity AS
SELECT
    severity,
    COUNT(*) AS total_accidents
FROM accidents
GROUP BY severity;

CREATE OR REPLACE VIEW vw_accidents_by_hour AS
SELECT
    EXTRACT(HOUR FROM accident_time) AS hour_of_day,
    COUNT(*) AS total_accidents
FROM accidents
GROUP BY EXTRACT(HOUR FROM accident_time)
ORDER BY hour_of_day;

CREATE OR REPLACE VIEW vw_vehicle_severity AS
SELECT
    v.vehicle_type,
    a.severity,
    COUNT(*) AS total
FROM vehicles v
JOIN accidents a
  ON v.accident_id = a.accident_id
GROUP BY v.vehicle_type, a.severity;

CREATE OR REPLACE VIEW vw_location_severity_agg AS
SELECT
    latitude,
    longitude,
    COUNT(*) AS total_accidents,
    SUM(CASE WHEN severity = 1 THEN 1 ELSE 0 END) AS fatal_accidents,
    SUM(CASE WHEN severity = 2 THEN 1 ELSE 0 END) AS serious_accidents,
    SUM(CASE WHEN severity = 3 THEN 1 ELSE 0 END) AS slight_accidents,
    (3 * SUM(CASE WHEN severity = 1 THEN 1 ELSE 0 END) +
     2 * SUM(CASE WHEN severity = 2 THEN 1 ELSE 0 END) +
     1 * SUM(CASE WHEN severity = 3 THEN 1 ELSE 0 END)) AS severity_score
FROM accidents
GROUP BY latitude, longitude;
