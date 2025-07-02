import pandas as pd
from faker import Faker
import random
from datetime import datetime

# Создаем экземпляр Faker для генерации данных
fake = Faker()

def generate_transactions(num_transactions: int = 5) -> pd.DataFrame:
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

if __name__ == "__main__":
    transactions_df = generate_transactions(10)
    print("Сгенерированные транзакции:")
    print(transactions_df)

