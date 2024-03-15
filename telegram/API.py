import os

import requests
from aiogram import Bot
from dotenv import load_dotenv

from telegram import keyboards

load_dotenv()

BASE_URL = 'http://' + os.getenv('LOCALHOST_IP') + '/api/v1'


# WORKER
def get_worker_list():
    url = f"{BASE_URL}/workers"
    response = requests.get(url=url)
    return response.json()


def get_worker_by_telegram(telegram_id):
    url = f"{BASE_URL}/worker_by_tg/{telegram_id}"
    response = requests.get(url=url)
    if response.status_code == 404:
        return None
    else:
        return response.json()


def post_worker_registration(name, surname, telephone, telegram_id):
    url = f"{BASE_URL}/worker_registration"
    data = {
        "name": name,
        "surname": surname,
        "telephone": telephone,
        "telegram_id": telegram_id
    }
    response = requests.post(url, data)
    if response.status_code == 201:
        return True
    else:
        return False


# OBJECT
def get_object_list():
    url = f"{BASE_URL}/objects"
    response = requests.get(url=url)
    return response.json()


def get_object_by_paginated_url(url):
    response = requests.get(url=url)
    return response.json()


# CATEGORY
def get_category_list_by_object_id(object_id):
    url = f"{BASE_URL}/object/{object_id}/categories/"
    response = requests.get(url=url)
    return response.json()


def get_category_list_by_paginated_url(url):
    response = requests.get(url=url)
    return response.json()


# TYPE OF WORK
def get_work_type_list_by_category_id(category_id):
    url = f"{BASE_URL}/work_types/category/{category_id}/"
    response = requests.get(url=url)
    return response.json()


def get_work_type_list_by_paginated_url(url):
    response = requests.get(url=url)
    return response.json()


def get_work_type_list_by_object_id(object_id):
    url = f"{BASE_URL}/work_types/object/{object_id}/"
    response = requests.get(url=url)
    return response.json()["work_types"]


async def post_work_type_create(category, name, measurement, created_by, bot: Bot, worker_tg):
    url = f"{BASE_URL}/work_types/create"
    data = {
        "category": category,
        "name": name,
        "measurement": measurement,
        "created_by": created_by,
    }
    response = requests.post(url, data)
    if response.status_code == 201:
        return True
    elif response.status_code == 400:
        if response.json().get("non_field_errors") == [
            "The fields work_type, date, worker must make a unique set."
        ]:
            await bot.send_message(worker_tg,
                                   text="⚠️Тип работ с данным названием для данной категории уже существует⚠️",
                                   reply_markup=keyboards.main_kb)
        else:
            await bot.send_message(worker_tg,
                                   text="⚠️Обратитесь к разработчику⚠️"
                                        f"\n ошибка - {response.json()}",
                                   reply_markup=keyboards.main_kb)
    else:
        return False


# MEASUREMENT

def get_measurement_list():
    url = f"{BASE_URL}/measurements"
    response = requests.get(url=url)
    return response.json()


# SHIFT
async def post_shift_creation(worker_id, worker_tg, date, work_type_id, value, bot: Bot):
    url = f"{BASE_URL}/shift_creation"
    data = {
        "worker": worker_id,
        "date": date,
        "work_type": work_type_id,
        "value": value
    }
    response = requests.post(url, data)
    if response.status_code == 201:
        return True
    elif response.status_code == 400:
        if response.json().get("non_field_errors") == [
            "The fields work_type, date, worker must make a unique set."
        ]:
            await bot.send_message(worker_tg,
                                   text="⚠️Вы уже подали отчёт с такой датой на данный тип работ⚠️",
                                   reply_markup=keyboards.main_kb)
    else:
        return False


# REPORT

def get_report_individual(object_id: int, worker_id: int):
    url = f"{BASE_URL}/report_worker_individual/{object_id}/{worker_id}/"
    response = requests.get(url=url)
    if response.status_code == 200:
        return True
    else:
        return False
