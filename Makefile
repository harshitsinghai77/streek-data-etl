install:
	poetry install

export_requirments:
	poetry export -f requirements.txt --output requirements.txt

deploy:
	git push heroku master

run_dev_server:
	uvicorn main:app --reload

runserver:
	uvicorn main:app --port 5000

docker_image:
	docker build -t cliff-app .

start_docker_container:
	docker run -d --name cliff-app -p 5000:5000 cliff-app

dump_sample_data:
	docker exec -i cliff-data-etl_postgresql_1 pg_restore -U cliff -v -d cliff < dev/dump/sample.dump

format:
	bash scripts/format.sh

test:
	pytest