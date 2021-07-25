pyenv virtualenv 3.9.6 cliff-venv

docker-compose up -d

docker exec -i cliff-data-etl_postgresql_1 pg_restore -U cliff -v -d cliff < sample.dump
