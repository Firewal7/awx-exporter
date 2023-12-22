## AWX Prometheus Exporter

#### Собираем образ:
```
docker build -t project/awx-exporter:latest .
```
#### Запускаем контейнер:

Все значения меняем на свои.
```
docker run -p 9191:9191 -e PORT=9191 -e URL=http://158.160.66.205:31796/ -e USERNAME=admin -e PASSWORD=x17urdvTv project/awx-exporter:latest

http://158.160.66.205:9191 
```