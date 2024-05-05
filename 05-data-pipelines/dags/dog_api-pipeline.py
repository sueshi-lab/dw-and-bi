import logging
import requests
import json

from airflow import DAG
from airflow.utils import timezone
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

def _get_dog_api():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    logging.info(data)
    with open("/opt/airflow/dags/dog.json","w") as f:
        json.dump(data, f)

def _move_file():
    import os
    os.system("mv /opt/airflow/dags/dog.json /path/to/doggy/")

with DAG(
    "dog_api_pipeline",
    start_date=timezone.datetime(2024, 3, 23),
    schedule="@daily",
    tags=["DS525"],
):
    start = EmptyOperator(task_id="start")

    get_dog_api = PythonOperator(
        task_id="get_dog_api",
        python_callable=_get_dog_api,
    )

    move_file = BashOperator(
        task_id="move_file",
        bash_command="_move_file",
    )

    end = EmptyOperator(task_id="end")

    start >> get_dog_api >> end