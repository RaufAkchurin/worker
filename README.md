Запуск контейнера с базой данных постгрес( будет одна, общая для телеграм бота и для джанго приложения(там у нас только админка))

```shell
sudo docker run -d \
-e POSTGRES_USER=worker_app \
-e POSTGRES_PASSWORD=worker_app \
-p 5432:5432 \
--name worker_app \
--restart always \
postgres:14.1-alpine
```