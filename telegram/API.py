import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def get_object_list():
    url = f"{BASE_URL}/object"
    response = requests.get(url=url)
    return response.json()
