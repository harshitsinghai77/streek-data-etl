install:
	poetry install

export_requirments.txt:
	poetry export -f requirements.txt --output requirements.txt

runserver:
	uvicorn main:app --reload --port 5000

docker_image:
	docker build -t streek-app .

start_docker_container:
	docker run -d --name streek-app -p 5000:5000 streek-app

restore_sample_data:
	docker exec -i streek-postgres pg_restore -U streek -v -d streek < dev/dump/sample.dump

dump_sample_data:
	pg_dump -O -f dev/dump/sample.sql postgres://streek:password@localhost:5432/streek

format:
	bash scripts/format.sh

test:
	pytest --cov=app 