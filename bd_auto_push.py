import hashlib
import time
from dotenv import load_dotenv
from github import Github
import os

load_dotenv()


def calculate_sha(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        # Читаем файл блоками по 4096 байт (4 КБ)
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def push_to_github(repo_path, github_token, commit_message):
    try:
        g = Github(github_token)
        repo = g.get_repo("RaufAkchurin/worker")

        branch = "master"  # Замените "master" на вашу ветку
        file_path = "db.sqlite3"
        full_path = os.path.join(repo_path, file_path)

        # Получение хэша последнего коммита в ветке
        sha = repo.get_branch(branch).commit.sha

        with open(full_path, 'rb') as file_content:
            content = file_content.read()

        # Получение нового SHA файла после модификации
        new_sha = calculate_sha(full_path)

        # Обновление файла с предоставлением нового SHA
        repo.update_file(file_path, commit_message, content, new_sha, branch=branch)

        print(f'Successfully pushed to GitHub at {time.ctime()}')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    REPO_PATH = '/root/worker'
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    COMMIT_MESSAGE = 'Update database automatic'

    push_to_github(REPO_PATH, GITHUB_TOKEN, COMMIT_MESSAGE)
