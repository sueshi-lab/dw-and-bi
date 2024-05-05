get docker-compose.yaml from https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.0/docker-compose.yaml'
```

change AIRFLOW__CORE__EXECUTOR from CeleryExecutor -> LocalExecutor
```yaml
AIRFLOW__CORE__EXECUTOR: LocalExecutor
```

comment unused config and services
```
#config
AIRFLOW__CELERY__RESULT_BACKEND
AIRFLOW__CELERY__BROKER_URL
redis config

#service
redis
airflow-worker
airflow-triggerer
flower
```

create my_first_dag.py in dags folder

check new dags in Airflow web service
tag name: DS525

