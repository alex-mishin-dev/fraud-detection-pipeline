SHELL := /bin/bash

# --- Базовые команды ---

# Запуск всех сервисов в фоновом режиме
up:
	docker compose up -d

# Остановка всех сервисов
down:
	docker compose down

# Полная очистка: остановка, удаление контейнеров и всех данных (volumes)
clean:
	docker compose down -v

# --- Команды для разработки ---

# Пересборка и запуск всех сервисов 
rebuild:
	docker compose up -d --build

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
	@docker exec -it spark-master /usr/local/spark/bin/spark-submit \
		--driver-memory 2g \
		--executor-memory 2g \
		/home/jovyan/work/src/spark_consumer.py

.PHONY: up down clean rebuild logs init-topic run-producer run-spark-consumer
