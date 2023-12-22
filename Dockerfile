# Используем официальный образ Ubuntu 20.04
FROM ubuntu:20.04

# Установка необходимых пакетов (если они еще не установлены)
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Создаем директорию /app
RUN mkdir /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Устанавливаем зависимости 
RUN pip3 install -r requirements.txt

# Команда запуска вашего проекта с использованием переменных среды
CMD ["python3", "export.py"]


 