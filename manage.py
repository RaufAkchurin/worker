#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worker.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# 8.11 - 3 Модели - архитектура
# 9.11 - 2 МОдели -архитектура
# 12.11 - 3 BOT первый запауск
# 13.11 - 5.5  постгресс
# 14.11 - 5 - модели
# 16.11 -9 админка + модели + Бот
# 17.11 - 5 (формирование отчёта)
# 18.11 - 2 (формирование отчёта)


# 30.11 11-40 -


# работа на 13.11
#
# сгенерить модели для алхимии в аиограм
#
# поднять отдельно постгре БД
#
# подключить джангу и аиограмм в БД
#
# убедиться что записи создаются/удаляются из обоих БД

