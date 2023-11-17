from pprint import pprint

import requests

BASE_URL = "http://localhost:8000/api/v1"


def get_object_list():
    url = f"{BASE_URL}/objects"
    response = requests.get(url=url)
    return response.json()


# сделать доступ по ключу объекты как ниже в категориях(править вьюху)


def get_category_list_by_object_id(object_id):
    url = f"{BASE_URL}/object/{object_id}/categories/"
    response = requests.get(url=url)
    return response.json()["categories"]


def get_work_type_list_by_category_id(category_id):
    url = f"{BASE_URL}/worktypes/category/{category_id}/"
    response = requests.get(url=url)
    return response.json()


def get_work_type_list_by_object_id(object_id):
    url = f"{BASE_URL}/work_types_by_object/{object_id}/"
    response = requests.get(url=url)
    return response.json()["work_types"]


# print(get_work_type_list_by_category_id(2))