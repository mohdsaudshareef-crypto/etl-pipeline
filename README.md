# ETL Pipeline Project

## What this does
An automated data pipeline that extracts electricity access data,
transforms and cleans it, and loads it into a SQLite database.

## Technologies Used
- Python
- Pandas
- SQLite
- Schedule
- Logging

## Pipeline Steps
1. Extract - reads CSV data
2. Transform - cleans and reshapes data
3. Load - saves to SQLite database
4. Orchestration - controls pipeline flow
5. Scheduling - runs automatically daily
6. Logging - records all activity