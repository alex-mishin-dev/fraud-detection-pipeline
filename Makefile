export DOCKER_GID := $(shell getent group docker | cut -d: -f3)

SHELL := /bin/bash

# --- Базовые команды ---

# Полное развертывание всей инфраструктуры с помощью Ansible
deploy:
	ansible-playbook playbook.yml

# Запуск всех сервисов в фоновом режиме
up:
	docker compose up -d

# Остановка всех сервисов
down:
	docker compose down

# Просмотр логов конкретного сервиса (например, make logs service=spark-master)
logs:
	docker logs $(service)

# --- Команды для пайплайна ---

# Инициализация: создание Kafka топика
init-topic:
	@echo "Creating Kafka topic 'transactions'..."
	@docker exec -it kafka kafka-topics --create --if-not-exists --topic transactions --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
	@echo "Topic 'transactions' is ready."

# Запуск генератора данных (продюсера)
run-producer:
	@echo "Starting data generator..."
	@source venv/bin/activate && python src/data_generator.py

# Запуск Spark-джобы (консьюмера)
run-spark-consumer:
	@echo "Submitting Spark job..."
	@docker exec spark-master /usr/local/spark/bin/spark-submit \
		--driver-memory 2g \
		--executor-memory 2g \
		/home/jovyan/work/src/spark_consumer.py

# Подключение к интерактивной сессии PostgreSQL. \dt SELECT * FROM fraudulent_transactions LIMIT 10; \q
db-shell:
	@echo "Connecting to PostgreSQL shell..."
	@docker exec -it fraud_db psql -U airflow

# Открытие веб-интерфейса Metabase
open-bi:
	@echo "Opening Metabase BI tool at http://localhost:3000"
	@python3 -m webbrowser http://localhost:3000

.PHONY: up down clean rebuild logs init-topic run-producer run-spark-consumer db-shell
