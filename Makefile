venv_start:
			source worker/venv/bin/activate

restart_server:
			sudo systemctl daemon-reload
			sudo systemctl stop worker
			sudo systemctl start worker

status_server:
			systemctl status worker.service

push_from_server:
			python3 bd_auto_push.py

.PHONY: restart_server status_server push_from_server