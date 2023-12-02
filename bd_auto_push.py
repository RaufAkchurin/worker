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

        # Получение хэша последнего коммита в ветке
        sha_latest_commit = repo.get_branch(branch).commit.sha

        with open(full_path, 'rb') as file_content:
            content = file_content.read().decode('utf-8')  # Декодируем содержимое файла

        # Получение текущего содержимого файла
        file_content_obj = repo.get_contents(file_path, ref=branch)
        content_latest_commit = file_content_obj.decoded_content.decode('utf-8')

        # Проверка, изменилось ли содержимое файла
        if content != content_latest_commit:
            # Обновление файла
            repo.update_file(
                file_path,
                commit_message,
                content,
                sha_latest_commit,  # Используем SHA последнего коммита
                branch=branch
            )

            print(f'Successfully pushed to GitHub at {time.ctime()}')
        else:
            print('No changes in the file. Skipping commit and push.')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    REPO_PATH = '/root/worker'
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    COMMIT_MESSAGE = 'Update database automatic'

    push_to_github(REPO_PATH, GITHUB_TOKEN, COMMIT_MESSAGE)
