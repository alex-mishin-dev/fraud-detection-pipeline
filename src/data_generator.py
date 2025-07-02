import pandas as pd
from faker import Faker
import random
from datetime import datetime
import json
from kafka import KafkaProducer


fake = Faker()
def generate_transactions() -> dict:
    return {
        'transaction_id': fake.uuid4(),
        'customer_id': fake.uuid4(),
        'amount': round(random.uniform(1.0, 5000.0), 2),
        'timestamp': datetime.now().isoformat(),
        'is_fraud': random.choices([0, 1], weights=[95, 5], k=1)[0]
    }


if __name__ == "__main__":
    
    # Создаем продюсера, который будет отправлять сообщения в Kafka
    producer = KafkaProducer(
        bootstrap_servers=['localhost:29092'], # Адрес нашего Kafka брокера
        value_serializer=lambda v: json.dumps(v).encode('utf-8') # Сериализуем сообщения в JSON
    )
    
    # Название "канала" или "очереди", куда мы будем публиковать транзакции
    KAFKA_TOPIC = "transactions"
    
    print("Начинаю отправку транзакций в Kafka. Нажми Ctrl+C для остановки.")
    try:
        # Бесконечный цикл для генерации потока данных
        while True:
            transaction = generate_transactions()
            producer.send(KAFKA_TOPIC, value=transaction)
            print(f"Отправлена транзакция: {transaction['transaction_id']}")
    except KeyboardInterrupt:
        print("Остановка генератора.")
    finally:
        
        producer.flush()
        producer.close()
        print("Соединение с Kafka закрыто.")
