                    Deploy  
1) Подключаемся к серверу ssh root@555.444.666.777

2) Клонируем репозиторий https://github.com/RaufAkchurin/worker

2) Создаём виртуальную среду

3) Запускаем её, накатываем все зависимости

4) Создаём .env и копируем туда данные свои
**ВНМИАНИЕ!!!**
-на серваке LOCALHOST_IP в .env указываем АЙПИ сервера
-на локальном компе указываем 127.0.0.1:8000

5) В settings.py проверяем наличие обоих АЙПИ **ALLOWED_HOSTS = ['АЙПИ СЕРВЕРА', '127.0.0.1']**

6) Запускаем джангу вот так 
**nohup python3 manage.py runserver 555.444.666.777:8000**
те при запуске надо указать настоящий айпи сервера

7) После закрытия терминала процесс будет жить, чтобы его найти в 
дальнейшем можно воспользоваться
**`ps aux | grep 'python3'`**

   8) чтобы завершить принудительно процесс, используй
   **`kill -9 PID`**
   Замените PID на фактический идентификатор процесса.

         _НАСТРОЙКА АВТОМАТИЧЕСКОГО РЕСТАРТА В СЛУЧАЕ ПАДЕНИЯ_


        НАСТРОЙКА systemctl (автоматический перезапуск в случае падения)

**Создайте файл службы:**
sudo nano /etc/systemd/system/worker.service


**Добавьте следующую конфигурацию в файл службы:**


[Unit]
Description=Django and Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/worker
ExecStart=/root/worker/venv/bin/python3 /root/worker/manage.py runserver 555.444.666.777:8000(вставить реальный)
KillMode=process
Restart=always
RestartSec=10
EnvironmentFile=/root/worker/.env
ExecStartPost=/root/worker/venv/bin/python3 /root/worker/telegram/bot.py

[Install]
WantedBy=multi-user.target



            **ПОСЛЕ ПАРВОК В КОНФИГЕ**
**sudo systemctl daemon-reload**
**sudo systemctl start worker**
статус проверять вот так **systemctl status worker.service**


      АВТОМАТИЧЕСКИЙ ПУШИНГ БАЗЫ НА ГИТХАБ НАСТРОЙКА

1) в .енв добавить токен от гитхаба
2) Для того чтобы скрипт выполнялся раз в день автоматически, вы можете использовать планировщик задач в операционной системе. Например, для Unix-подобных систем (Linux, macOS) это может быть cron.

Вот пример того, как вы можете настроить cron-задачу:

Откройте терминал.

Введите команду:

`crontab -e`
В редакторе cron-задач добавьте строку, которая будет запускать ваш скрипт раз в день. Например:

`0 13 * * * /root/worker/venv/bin/python3 /root/worker/bd_auto_push.py`
Эта строка означает, что скрипт будет запускаться каждый день в (13 часов, 0 минут). Вы можете изменить время запуска, используя другие значения.

Сохраните изменения и закройте редактор.
Таким образом, ваш скрипт будет выполняться ежедневно по заданному расписанию. Убедитесь, что пути к интерпретатору Python (python3) и вашему скрипту (bd_auto_push.py) указаны правильно в команде cron.


               НАСТРОЙКА ГУВИКОРНА ЧТОБЫ РАБОТАЛ ЧЕРЕЗ ДОМЕН МНЕСТО АПИ

создаём /etc/nginx/sites-available/myproject

добавляем  конфиг

server {
    listen 80;
    server_name 31.129.103.105 rting-erp.ru;   # наш домен, и айпи адрес сервера где крутится приложение

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /root/worker;
    }

    location /media/ {
        root /root/worker;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

                        NGINX

/etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
	worker_connections 768;
	# multi_accept on;
}

http {

	##
	# Basic Settings
	##

	sendfile on;
	tcp_nopush on;
	types_hash_max_size 2048;
	# server_tokens off;

	# server_names_hash_bucket_size 64;
	# server_name_in_redirect off;

	include /etc/nginx/mime.types;
	default_type application/octet-stream;

	##
	# SSL Settings
	##

	ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
	ssl_prefer_server_ciphers on;

	##
	# Logging Settings
	##

	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	##
	# Gzip Settings
	##

	gzip on;

	# gzip_vary on;
	# gzip_proxied any;
	# gzip_comp_level 6;
	# gzip_buffers 16 8k;
	# gzip_http_version 1.1;
	# gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

	##
	# Virtual Host Configs
	##

	include /etc/nginx/conf.d/*.conf;
	include /etc/nginx/sites-enabled/*;
}





