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


