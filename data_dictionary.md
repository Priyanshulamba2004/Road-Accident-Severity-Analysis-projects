# Road Accident Severity Analysis - Data Dictionary

## accidents.csv

| Column           | Type    | Description                                  |
|------------------|---------|----------------------------------------------|
| accident_id      | string  | Unique ID for each reported accident         |
| accident_date    | date    | Date of the accident                         |
| accident_time    | string  | Time of the accident (HH:MM, 24-hour)        |
| latitude         | float   | Latitude coordinate of the accident location |
| longitude        | float   | Longitude coordinate of the accident location|
| severity         | int     | 1=Fatal, 2=Serious, 3=Slight                 |
| weather          | string  | Weather condition at time of accident        |
| light_conditions | string  | Lighting condition (Daylight/Night/Sunset)   |
| road_type        | string  | Type of road (Highway/Crossroad/etc.)        |
| city             | string  | City where accident occurred                 |
| state            | string  | State where accident occurred                |

## vehicles.csv

| Column         | Type    | Description                                      |
|----------------|---------|--------------------------------------------------|
| accident_id    | string  | Links to the primary accident record             |
| vehicle_id     | string  | Unique ID of the vehicle in that accident        |
| vehicle_type   | string  | Type of vehicle (Car/Bike/Truck/Bus/Auto)        |
| age_of_driver  | int     | Age of the driver at the time of the accident    |
