clean_migrations:
			find worker_app/migrations/ -type f ! -name '__init__.py' -exec rm -f {} +
			rm -rf worker_app/migrations/__pycache__

clean_db:
		 rm -f db.sqlite3

create_migrations:
			./manage.py makemigrations
			./manage.py migrate
			./manage.py createsuperuser --username admin

rebuild_db_localhost:
			make clean_migrations
			make clean_db
			make create_migrations
			./manage.py runserver

.PHONY: clean_migrations clean_db restart_db