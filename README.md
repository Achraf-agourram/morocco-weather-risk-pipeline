# Morocco Weather Risk Pipeline

An automated weather-risk ETL pipeline for Moroccan cities. The project extracts city and weather data, cleans and transforms it, engineers weather-risk features, stores the results in PostgreSQL, and provides a Streamlit dashboard for monitoring upcoming weather risks.

## Project Objective

The pipeline is designed to answer the business question:

> **Where and when should we be particularly vigilant in the next few days?**

The dashboard combines weather forecasts with a 0–100 weather risk score based on precipitation, wind, temperature, and precipitation probability.

## Architecture

```text
SimpleMaps
    |
    v
City extraction
    |
    +----------------------+
    |                      |
    v                      v
Open-Meteo            Cities data
Weather extraction
    |
    v
Bronze
    |
    v
Silver
Cleaning + validation + city join
    |
    v
Gold
Feature engineering + risk score
    |
    v
PostgreSQL
    |
    +-------------------+
    |                   |
    v                   v
Airflow            Streamlit
Orchestration      Dashboard
```

## Technologies

- Python
- Pandas
- Requests
- PostgreSQL
- psycopg2
- Apache Airflow
- Streamlit
- PyDeck
- Docker
- Docker Compose

## Data Sources

### SimpleMaps

Used to obtain Moroccan city information and coordinates.

- Source: SimpleMaps Morocco Cities
- Data stored in: `data/bronze/cities.csv`

### Open-Meteo

Used to obtain daily weather forecasts.

The extracted forecast data includes:

- Maximum temperature
- Minimum temperature
- Precipitation
- Precipitation probability
- Maximum wind speed
- Maximum wind gusts
- Weather code
- Forecast date
- Latitude and longitude

Raw data is stored in:

```text
data/bronze/weather.json
```

## Project Structure

```text
.
├─ dags
│  └─ weather_pipeline_dag.py
│
├─ data
│  ├─ bronze
│  │  ├─ cities.csv
│  │  └─ weather.json
│  ├─ gold
│  │  └─ weather_features.csv
│  └─ silver
│     └─ clean_weather.csv
│
├─ docker
│  ├─ airflow
│  │  ├─ Dockerfile
│  │  └─ requirements.txt
│  └─ streamlit
│     └─ Dockerfile
│
├─ docs
│  └─ weather_pipeline.jpg
│
├─ sql
│  ├─ 01-create-airflow-db.sql
│  └─ 02-schema.sql
│
├─ src
│  ├─ analytics
│  │  └─ analytics.py
│  ├─ transformation
│  │  ├─ cleaning.py
│  │  ├─ features.py
│  │  └─ validating.py
│  ├─ database.py
│  ├─ extraction.py
│  └─ loading.py
│
├─ app.py
├─ compose.yaml
├─ requirements.txt
├─ .dockerignore
└─ .env
```

Generated `__pycache__` folders and `.pyc` files are not part of the application logic and are ignored by the project configuration.

## Pipeline

### 1. Extraction

The extraction layer gets:

- Moroccan cities from SimpleMaps
- Weather forecasts from Open-Meteo

The raw outputs are stored in the Bronze layer:

```text
data/bronze/cities.csv
data/bronze/weather.json
```

### 2. Silver: Cleaning and Transformation

The Silver layer performs:

- Data type standardization
- Date conversion
- Duplicate detection and treatment
- Data consistency checks
- Data quality validation
- City/weather joining using geographic coordinates

Output:

```text
data/silver/clean_weather.csv
```

### 3. Gold: Feature Engineering

The Gold layer creates:

- Temperature categories
- Precipitation categories
- Wind categories
- Date features
- Rain risk
- Wind risk
- Temperature risk
- Rain probability risk
- Weather risk score
- Risk category

Output:

```text
data/gold/weather_features.csv
```

### 4. Weather Risk Score

The project uses a score between 0 and 100.

The main components are weighted as follows:

| Component | Weight |
|---|---:|
| Precipitation risk | 35% |
| Wind risk | 35% |
| Temperature risk | 15% |
| Rain probability risk | 15% |

Formula:

```text
Weather Risk Score =
    Rain Risk × 0.35
  + Wind Risk × 0.35
  + Temperature Risk × 0.15
  + Rain Probability Risk × 0.15
```

The score is classified into:

| Score | Category |
|---:|---|
| 0–25 | low |
| 25–50 | moderate |
| 50–75 | high |
| 75–100 | very_high |

The thresholds are project-defined operational thresholds used to support the dashboard's risk interpretation.

## PostgreSQL

The database contains three main application tables:

### `cities`

Stores Moroccan city information and coordinates.

### `weather_forecasts`

Stores forecast values for each city and date.

A unique constraint on:

```text
(city_id, forecast_date)
```

prevents duplicate forecast rows and allows forecasts to be updated on later runs.

### `weather_risks`

Stores the risk components, final risk score, and risk category.

It is linked to `weather_forecasts` through `forecast_id`.

The database schema is defined in:

```text
sql/02-schema.sql
```

Airflow metadata is stored separately in:

```text
airflow_db
```

and initialized through:

```text
sql/01-create-airflow-db.sql
```

## Analytics

The analytics module provides SQL-based analysis for questions such as:

- Which cities have the highest maximum temperatures?
- Which cities have the highest daily precipitation?
- Which cities have the highest average weather risk?
- Which forecast dates have the highest average risk?
- What is the highest-risk period for each city?

For precipitation:

- `MAX(precipitation)` identifies the highest daily precipitation.
- `SUM(precipitation)` identifies the total precipitation accumulated over the selected period.

## Streamlit Dashboard

The dashboard is implemented in:

```text
app.py
```

It connects to PostgreSQL and displays:

### KPIs

- Number of cities
- Maximum temperature
- Maximum precipitation
- Number of risk periods
- City with the highest risk

### Filters

- City
- Date / period
- Risk level

### Visualizations

- Weather-risk map
- Risk evolution
- Temperature evolution
- Precipitation
- Risk-period table

The risk map uses latitude and longitude with PyDeck. Map points are colored according to the risk level.

The dashboard is designed to quickly identify:

- **Where** the risk is located
- **When** the risk is expected
- **How high** the risk is
- **Which weather factors** contribute to the situation

## Airflow Orchestration

The DAG is located at:

```text
dags/weather_pipeline_dag.py
```

The workflow is organized as:

```text
Extract cities
       |
Extract weather
       |
       v
Transform / clean
       |
       v
Feature engineering
       |
       v
Load PostgreSQL
       |
       v
Refresh / verify dashboard data
```

The DAG is scheduled daily and uses retries to handle temporary task failures.

## Docker

The project is containerized with Docker Compose.

Main services:

- PostgreSQL
- Airflow
- Streamlit

### Build the project

From the project root:

```bash
docker compose build
```

### Start all services

```bash
docker compose up
```

Or run them in the background:

```bash
docker compose up -d
```

### Check running services

```bash
docker compose ps
```

### View logs

```bash
docker compose logs airflow
```

```bash
docker compose logs streamlit
```

```bash
docker compose logs postgres
```

### Stop the project

```bash
docker compose down
```

The PostgreSQL data is stored in a Docker volume so that normal container recreation does not remove the database.

## Accessing the Services

When the containers are running:

### Streamlit

```text
http://localhost:8501
```

### Airflow

```text
http://localhost:8080
```

### PostgreSQL

```text
localhost:5432
```

Inside Docker, application containers connect to PostgreSQL through the Compose service name:

```text
postgres
```

rather than `localhost`.

## Environment Variables

The project uses a `.env` file for configuration.

Typical database variables are:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=weather_db

AIRFLOW_DB=airflow_db

DB_HOST=postgres
DB_PORT=5432
DB_NAME=weather_db
DB_USER=postgres
DB_PASSWORD=your_password
```

The real `.env` file should not be committed to Git.

## Local Development Without Docker

The Python source code can also be run directly on the local machine using the root `requirements.txt`.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
python -m streamlit run app.py
```

Docker is recommended for running the complete PostgreSQL + Airflow + Streamlit environment consistently.

## Main Files

| File | Role |
|---|---|
| `src/extraction.py` | Extracts city and weather data |
| `src/transformation/cleaning.py` | Cleans and transforms data |
| `src/transformation/validating.py` | Performs data validation |
| `src/transformation/features.py` | Creates weather features and risk score |
| `src/loading.py` | Loads data into PostgreSQL |
| `src/database.py` | Database connection and database operations |
| `src/analytics/analytics.py` | Analytical SQL queries |
| `dags/weather_pipeline_dag.py` | Airflow orchestration |
| `app.py` | Streamlit dashboard |
| `compose.yaml` | Docker Compose services |
| `sql/02-schema.sql` | Application database schema |
| `sql/01-create-airflow-db.sql` | Airflow database initialization |

## Pipeline Layers

```text
BRONZE
Raw extracted data
    ↓
SILVER
Cleaned and validated data
    ↓
GOLD
Features + risk score
    ↓
POSTGRESQL
Structured application data
    ↓
STREAMLIT
Visualization and monitoring
```

## Goal

The final system automates the complete weather-risk workflow for Moroccan cities:

```text
Extract
  ↓
Clean
  ↓
Validate
  ↓
Transform
  ↓
Engineer features
  ↓
Calculate risk
  ↓
Load PostgreSQL
  ↓
Visualize with Streamlit
```

Airflow automates the workflow, PostgreSQL stores the structured data, and Streamlit provides the dashboard used to monitor upcoming weather risks.
