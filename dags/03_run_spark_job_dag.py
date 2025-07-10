from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="03_run_spark_job_dag",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    schedule=None,  # будем запускать вручную
    tags=["spark", "pipeline"],
) as dag:
    # запускает нашу Spark-джобу через Makefile
    submit_spark_job = BashOperator(
        task_id="submit_spark_job_to_cluster",
        bash_command="make run-spark-consumer",
        cwd="/opt/airflow",
    )
