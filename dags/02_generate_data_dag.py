from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="02_generate_data_dag",
    description="A simple DAG to generate synthetic transaction data.",
    schedule="@daily",  
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["data_generation"],
) as dag:
    
    generate_data_task = BashOperator(
        task_id="generate_data",
        bash_command="python /opt/airflow/src/data_generator.py",
    )
