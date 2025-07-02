import pandas as pd
from faker import Faker
import random
from datetime import datetime
import os

# Создаем экземпляр Faker для генерации фейковых данных
fake = Faker()

def generate_transactions(num_transactions: int = 10) -> pd.DataFrame:
    """
    Генерирует DataFrame с фейковыми банковскими транзакциями.

    Args:
        num_transactions (int): Количество транзакций для генерации.

    Returns:
        pd.DataFrame: DataFrame с данными о транзакциях.
    """
    data = []
    for _ in range(num_transactions):
        transaction = {
            'transaction_id': fake.uuid4(),
            'customer_id': fake.uuid4(),
            'amount': round(random.uniform(1.0, 5000.0), 2),
            'timestamp': datetime.now().isoformat(),
            'is_fraud': random.choices([0, 1], weights=[95, 5], k=1)[0]
        }
        data.append(transaction)
    
    df = pd.DataFrame(data)
    return df

# Этот блок выполнится только тогда, когда мы запускаем этот файл напрямую
if __name__ == "__main__":
    
    # Определяем путь для сохранения данных ВНУТРИ контейнера
    output_dir = "/opt/airflow/data"
    output_path = os.path.join(output_dir, "transactions.csv")

    # Создаем папку data внутри контейнера, если ее нет
    os.makedirs(output_dir, exist_ok=True)
    
    # Генерируем данные
    transactions_df = generate_transactions(15)
    
    # Сохраняем DataFrame в CSV-файл
    transactions_df.to_csv(output_path, index=False)
    
    print(f"Сгенерированные транзакции сохранены в {output_path}")

