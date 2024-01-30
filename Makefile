
all:
	@echo "Subhan lah"

deploy:
	docker compose -f docker-compose.yaml up --build -d

develop:
	docker compose -f docker-compose.dev.yaml up --build -d

deploy-down:
	docker compose -f docker-compose.yaml down --rmi all -v

develop-down:
	docker compose -f docker-compose.dev.yaml down --rmi all -v

develop-re: develop-down develop

deploy-re: deploy-down deploy

logs:
	docker-compose logs -f

reset-db:
	rm -f services/authentication/db.sqlite3 services/player/db.sqlite3

re: down all
