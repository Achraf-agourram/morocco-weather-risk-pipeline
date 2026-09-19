from src.extraction  import *
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta



with DAG(
    dag_id="weather_pipeline",
    default_args={"owner": "weather_pipeline", "retries": 2, "retry_delay": timedelta(minutes=3)},
    description="Daily Moroccan weather risk pipeline",
    schedule="@daily",
    start_date=datetime(2026, 9, 18),
    catchup=False
) as dag:
    
    extract_cities_task = PythonOperator(task_id="extract_cities", python_callable=extract_cities)
    extract_weather_task = PythonOperator(task_id="extract_weather", python_callable=extract_weather)

    transform_clean_task = BashOperator(task_id="trans_clean_data", bash_command="python /opt/airflow/src/transformation/cleaning.py")
    feature_engineering_task = BashOperator(task_id="features_eng", bash_command="python /opt/airflow/src/transformation/features.py")

    loading_task = BashOperator(task_id="load_data", bash_command="python /opt/airflow/src/loading.py")

    extract_cities_task >> extract_weather_task >> transform_clean_task >> feature_engineering_task >> loading_task