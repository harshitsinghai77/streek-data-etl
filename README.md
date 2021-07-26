pyenv install 3.9.5
pyenv virtualenv 3.9.5 cliff-venv

docker-compose up -d

docker exec -i cliff-data-etl_postgresql_1 pg_restore -U cliff -v -d cliff < sample.dump

docker run -d -p 5000:5000 --name cliff-app harshitsinghai77/cliff-ai:latest

# Get started

## Installation

### Install with Docker (highly recommended)

```bash
docker run -d -p 5000:5000 --name cliff-app harshitsinghai77/cliff-ai:latest
```

The docker container assumes Postgres running in the IP Address. To change the IP Address, SSH into the container and change `DB_HOST` in the `.env` file.

### Install for development

```shell
git clone https://github.com/harshitsinghai77/cliff-ai-data-etl.git

cd cliff-ai-data-etl
```

Rename `.env.example` to `.env`

```shell
cp .env.example .env
```

Make sure you have pyenv and poetry installed

```shell
pyenv install 3.9.5
pyenv virtualenv 3.9.5 cliff-venv
```

Create a file named `.python-version` with content `cliff-venv` that way your virtual environment will automatically get activated when you `cd` into `cliff-ai-data-etl` directory. If for some reason your auto-activation is not working then you can manually activate using `pyenv activate cliff-venv`.

### Install dependencies

```shell
make install
```

or you can directly use

```shell
poetry install
```

### Setting up the database

The project depends on Postgres database running inside a docker container.

To easily setup the postgres database, use

```bash
docker-compose up -d
```

This will download `postgres:13` image, start the container and expose it to port `5432`

To check if the container is running

```shell
docker ps -a
```

Postgres credentials

```yaml
POSTGRES_DB: "cliff"
POSTGRES_USER: "cliff"
POSTGRES_PASSWORD: "password"
```

For more details, check `docker-compose.yml` in the root directory.
