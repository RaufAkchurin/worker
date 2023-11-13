import requests
import json

BASE_URL = "http://localhost:8000/api/v1"


def create_category(name):
    url = f"{BASE_URL}/category"
    post = requests.post(url=url, data={"name": name})
    print(post)


create_category("from_function")
