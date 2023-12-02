import time
from dotenv import load_dotenv
from github import Github
import os
from git import Repo

load_dotenv()


def push_to_github(repo_path, github_token, commit_message):
    try:
        g = Github(github_token)
        repo = g.get_repo("RaufAkchurin/worker")

        branch = "master"  # Замените "master" на вашу ветку

        # Инициализация объекта Git для репозитория
        git_repo = Repo(repo_path)

        # Проверка статуса репозитория
        if git_repo.is_dirty(untracked_files=True):
            # Получение хэша последнего коммита в ветке
            sha_latest_commit = repo.get_branch(branch).commit.sha

            # Проверка, является ли файл db.sqlite3 неотслеживаемым
            untracked_files = git_repo.untracked_files
            if "db.sqlite3" in untracked_files:
                # Обновление файла
                with open(os.path.join(repo_path, "db.sqlite3"), 'rb') as file_content:
                    content = file_content.read()

                repo.update_file(
                    "db.sqlite3",
                    commit_message,
                    content,
                    sha_latest_commit,  # Используем SHA последнего коммита
                    branch=branch
                )

                print(f'Successfully pushed to GitHub at {time.ctime()}')
            else:
                print('db.sqlite3 is not an untracked file. Skipping commit and push.')
        else:
            print('No changes in the repository. Skipping commit and push.')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == "__main__":
    REPO_PATH = '/root/worker'
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    COMMIT_MESSAGE = 'Update database automatic'

    push_to_github(REPO_PATH, GITHUB_TOKEN, COMMIT_MESSAGE)
