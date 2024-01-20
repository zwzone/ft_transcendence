
all:
	@echo "Subhan lah"

deploy:
	docker compose -f docker-compose.yaml up --build -d

develop:
	docker compose -f docker-compose.dev.yaml up --build -d

deploy-down:
	docker compose -f docker-compose.yaml down --rmi all -v

develop-down:
	docker compose -f docker-compose.dev.yaml down

re: down all
