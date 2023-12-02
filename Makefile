restart_server:
			sudo systemctl daemon-reload
			sudo systemctl stop worker
			sudo systemctl start worker
			systemctl status worker.service

push_from_server:
			python3 bd_auto_push.py

.PHONY: restart_server push_from_server