from prometheus_client import start_http_server, Metric, REGISTRY
import requests
import os
import re
import time

def sanitize_name(name):
    # Заменяем недопустимые символы в именах метрик
    return re.sub(r'[^a-zA-Z0-9:_]', '_', name)

class JsonCollector(object):
    def __init__(self, endpoint, username, password):
        self._endpoint = f"{endpoint.rstrip('/')}/api/v2/metrics/"
        self._auth = (username, password)

    def collect(self):
        # Получаем метрики Prometheus
        response = requests.get(self._endpoint, auth=self._auth, verify=False)

        if response.status_code != 200:
            print(f"Ошибка: Запрос API вернул код состояния {response.status_code}")
            return

        # Обрабатываем каждую строку в ответе
        for line in response.text.split('\n'):
            if line.startswith('#') or not line.strip():
                # Пропускаем комментарии и пустые строки
                continue

            # Разбиваем каждую строку на имя, значение и метки
            parts = line.split()
            name = parts[0]
            value = float(parts[1])
            labels = {}

            # Разбираем метки, если они существуют
            if len(parts) > 2:
                for label in parts[2:]:
                    label_name, label_value = label.split('=')
                    # Заменяем недопустимые символы в именах меток
                    label_name = sanitize_name(label_name)
                    labels[label_name] = label_value

            # Создаем метрику Prometheus с допустимым именем
            metric_name = sanitize_name(f"tower_{name}")
            metric = Metric(metric_name, '', 'gauge')
            metric.add_sample(metric_name, value=value, labels=labels)

            # Передаем метрику в Prometheus
            yield metric

if __name__ == '__main__':
    # Устанавливаем значения конфигурации из переменных окружения
    port = int(os.environ.get('PORT'))
    endpoint = os.environ.get('URL')
    username = os.environ.get('USERNAME')
    password = os.environ.get('PASSWORD')

    # Использование: python script.py
    start_http_server(port)
    REGISTRY.register(JsonCollector(endpoint, username, password))

    while True:
        time.sleep(1)
