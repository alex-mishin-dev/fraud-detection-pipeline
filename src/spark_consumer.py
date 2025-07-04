from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType

def process_batch(df: DataFrame, epoch_id: int):
    """
    Функция, которая будет применяться к каждому микро-батчу данных из Kafka.
    """
    print(f"--- Processing batch {epoch_id} ---")

    # Проверяем, пустой ли DataFrame, чтобы не делать лишней работы
    if df.count() == 0:
        print("Batch is empty, skipping.")
        return

    # 1. Наша бизнес-логика: отфильтровываем только мошеннические транзакции
    fraudulent_transactions = df.filter(col("is_fraud") == 1)
    
    # Если мошеннических транзакций нет, выходим
    if fraudulent_transactions.count() == 0:
        print("No fraudulent transactions in this batch.")
        return

    print(f"Found {fraudulent_transactions.count()} fraudulent transactions. Saving to PostgreSQL...")
    
    # Показываем, что мы собираемся записать
    fraudulent_transactions.show(truncate=False)

    # 2. Настройка подключения к PostgreSQL
    db_properties = {
        "user": "airflow",
        "password": "airflow",
        "driver": "org.postgresql.Driver"
    }
    db_url = "jdbc:postgresql://fraud_db:5432/airflow"
    
    # 3. Записываем отфильтрованный DataFrame в таблицу PostgreSQL
    # 'append' - добавлять данные, не перезаписывая таблицу
    fraudulent_transactions.write \
        .jdbc(url=db_url,
              table="fraudulent_transactions",
              mode="append",
              properties=db_properties)
    
    print("Successfully saved to PostgreSQL.")


def main():
    """
    Основная функция для запуска Spark Streaming Job.
    """
    spark = SparkSession.builder \
        .appName("TransactionConsumer") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # Схема наших данных в Kafka
    schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("amount", FloatType(), True),
        StructField("timestamp", StringType(), True),
        StructField("is_fraud", IntegerType(), True),
    ])

    # Читаем данные из Kafka
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "transactions") \
        .option("startingOffsets", "earliest") \
        .load()

    # Преобразуем JSON из Kafka
    json_df = kafka_df.selectExpr("CAST(value AS STRING) as json_string") \
        .select(from_json(col("json_string"), schema).alias("data")) \
        .select("data.*")

    # Вместо вывода в консоль, используем foreachBatch для записи в базу
    query = json_df.writeStream \
        .foreachBatch(process_batch) \
        .start()

    print("Spark Streaming job is running. Waiting for data to save to PostgreSQL...")
    query.awaitTermination()

if __name__ == "__main__":
    main()
