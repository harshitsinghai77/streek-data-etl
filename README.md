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

You can also use the script to create venv using virtualenv

```
bash scripts/create_virtualenv.sh
```

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

#### Postgres credentials

```yaml
POSTGRES_DB: "cliff"
POSTGRES_USER: "cliff"
POSTGRES_PASSWORD: "password"
```

To check if the container is running, run

```shell
docker ps -a
```

For more details, check `docker-compose.yml` in the root directory.

### Dump data to Postgres container

Sample data consist of a list of ~5000 e-commerce products and its information. The data can be downloaded [here](https://drive.google.com/file/d/1m0cF742dliCvnbmE3lc-WwxfZNbaikup/view)

#### Dump data in Postgres docker container using any of the following two methods

1. via `pg_dump`
2. via `python script`

### Dump csv data via pg_dump (Recommended)

```bash
make restore_sample_data
```

This will ssh into the postgres docker container and then dump data from `dev/dump/sample.dump`

### Dump csv data via python script.

First run the server using

```bash
make runserver
```

Then stop the server and run

```bash
python scripts/data_dump.py
```

Run `scripts/data_dump.py` only after running the server. This will make sure the tables are created and then the script will load the `.csv` and copy it to `core_item` table.

## Run Server

```bash
make runserver
```

or use

```bash
uvicorn main:app --reload
```

## Access APIs on localhost

```bash
make runserver
```

and go to
http://127.0.0.1:5000/docs

to use the APIs to list, add, delete or update products.

## Test the endpoints

To test endpoints either run `tests` with

```bash
make test
```

Or test it via the UI by running the server using

```bash
make runserver
```

and go to http://127.0.0.1:5000/docs

to test the endpoints via web UI.

![Swagger Documentation](https://i.ibb.co/891nKrk/cliff-ai-api-screenshot.png)

## API Documentation

For API documentation go to
http://127.0.0.1:5000/redoc

![Redoc documentation](https://i.ibb.co/zRjn3Dk/cliff-redoc-documentation.png)

## Testing

```bash
make test
```

Test coverage `98%`

## Deploy using Docker

Before creating the docker image, edit the `.env` file and change `DB_HOST` to your machine IP address.

`DB_HOST==<LOCAL-IP>`

For example `DB_HOST=192.168.29.63`

This is because localhost is not accessible from inside the Docker container. Thus, cliff docker container will not be able to access the Postgres container and the app will crash.

Change `DB_HOST` in `.env` to point to your IP address and then create a docker image using

```bash
make docker_image
```

Run the container using

```bash
make start_docker_container
```

To verify if everything is working fine, go to
http://127.0.0.1:5000/

and access the web API UI from
http://127.0.0.1:5000/docs

Test endpoint to verify the app is working and the API are served from the docker container.

## Format

```bash
make format
```

## CD using GitHub Actions

Github Actions are used for Continuous Delivery and Continuous Integration.

Github Actions will be triggered on every pull request. Edit the `.github/workflows/ci.yml` if required.

Check https://github.com/harshitsinghai77/cliff-ai-data-etl/actions

![Github Action](https://i.ibb.co/h8ssSPV/cliff-github-actions.png)

Github workflow consists of installing Postgres service, installing dependencies, dumping sample data to Postgres, running tests, formatting code, authenticating to DockerHub, creating a docker image and pushing the image to DockerHub.

## Add Secrets to Github Repo

In GitHub, browse your repository, select Settings > Secrets > Add a new secret.

Get access token from [DockerHub](https://hub.docker.com/).

Create two secrets `DOCKER_HUB_ACCESS_TOKEN` and `DOCKER_HUB_USERNAME`

Github Action will get the secrets from here when authenticating with DockerHub to automatically push the image to DockerHub.

## Automatically Publish the container to Docker Hub

Publish the image after it builds. Docker Hub support for Github Actions is straightforward, and all it requires is to create a token and then save it as a Github project secret, along with your Docker Hub username.
