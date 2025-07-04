from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType

def main():
    """
    Основная функция для запуска Spark Streaming Job.
    """
    spark = SparkSession.builder \
        .appName("TransactionConsumer") \
        .getOrCreate()

    # Скроем лишние логи, оставив только ошибки
    spark.sparkContext.setLogLevel("ERROR")

    # Схема данных в Kafka
    schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("amount", FloatType(), True),
        StructField("timestamp", StringType(), True),
        StructField("is_fraud", IntegerType(), True),
    ])

    # Читаем данные из Kafka как стриминговый DataFrame
    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "transactions") \
        .option("startingOffsets", "earliest") \
        .load()

    # Преобразуем бинарное значение из Kafka в строку и парсим JSON
    json_df = kafka_df.selectExpr("CAST(value AS STRING) as json_string") \
        .select(from_json(col("json_string"), schema).alias("data")) \
        .select("data.*")

    # Выводим результат в консоль (для проверки)
    query = json_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .option("truncate", "false") \
        .start()

    print("Spark Streaming job is running. Waiting for data...")
    query.awaitTermination()

if __name__ == "__main__":
    main()

