FROM apache/airflow:2.8.1

# Объявляем аргумент, который мы будем получать из docker-compose.yml
ARG DOCKER_GID

# Переключаемся на root ТОЛЬКО для системных задач
USER root

# Устанавливаем make
RUN apt-get update && \
  apt-get install -y --no-install-recommends make && \
  apt-get clean

# Создаем группу 'docker' ВНУТРИ контейнера с тем же GID, что и на ХОСТЕ
# И добавляем пользователя 'airflow' в эту группу
# Проверяем, что DOCKER_GID был передан
RUN if [ -z "$DOCKER_GID" ]; then \
  echo "Error: DOCKER_GID is not set."; \
  exit 1; \
  else \
  groupadd -g "$DOCKER_GID" docker && \
  usermod -aG docker airflow; \
  fi

# ПЕРЕКЛЮЧАЕМСЯ ОБРАТНО на пользователя airflow ПЕРЕД работой с pip
USER airflow

# Копируем requirements.txt
COPY requirements.txt /requirements.txt

# Теперь pip запускается от правильного пользователя
RUN pip install --no-cache-dir -r /requirements.txt
