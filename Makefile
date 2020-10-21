migrate:
	docker-compose up -d --build
	docker exec -t web python manage.py migrate
	docker-compose down
lint:
	docker exec -t web flake8 ./app
test:
	docker-compose up -d
	docker exec -t web python manage.py test tests
	docker-compose down