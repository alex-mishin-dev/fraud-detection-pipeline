# Импортируем библиотеки
from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

# Определяем DAG
with DAG(
    dag_id="01_hello_world_dag",
    description="My first DAG. It's rock-n-roll!",
    schedule=None,  
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"), 
    catchup=False, 
    tags=["hello_world", "tutorial"],
) as dag:
    # Создаем задачу 
        say_hello_task = BashOperator(
        task_id="say_hello",
        bash_command='echo "What\'s up, world? Airflow is ready to rock!"',
    )
