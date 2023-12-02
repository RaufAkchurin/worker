import time
from dotenv import load_dotenv
from github import Github
import os

load_dotenv()


def push_to_github(repo_path, github_token, commit_message):
    try:
        g = Github(github_token)
        repo = g.get_repo("RaufAkchurin/worker")

        branch = "master"  # Замените "master" на вашу ветку
        file_path = "db.sqlite3"
        full_path = os.path.join(repo_path, file_path)

        with open(full_path, 'rb') as file_content:
            content = file_content.read()

        # Создание файла без предоставления sha
        repo.create_file(file_path, commit_message, content, branch=branch)

        print(f'Successfully pushed to GitHub at {time.ctime()}')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    REPO_PATH = '/root/worker'
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    COMMIT_MESSAGE = 'Update database automatic'

    push_to_github(REPO_PATH, GITHUB_TOKEN, COMMIT_MESSAGE)
