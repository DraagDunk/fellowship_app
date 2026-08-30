# Fantasy Fellowship Book Club Application

A simple django app in docker.

## How to

### Development

To run the application locally, simply run

```bash
docker compose -f docker-compose.dev.yml up -d
```

and navigate to `localhost:8000`.

If you have not run the application before, you may need to build it first:

```bash
docker compose docker-compose.dev.yml build
```

and then migrate after the containers are up:

```bash
docker compose exec fellowship_app python3 manage.py migrate
```

If you want to install python dependencies locally (for the sake of your IDE for example), start a virtual environment before installing using pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Installing new dependencies

If you are running in a virtual environment (you should be), then you can install new dependencies with

```bash
pip install <package>
```

then add it to the requirements.txt file using

```bash
pip freeze > requirements.txt
```

## Environment variables

Here you can read about the environment variables used by the docker container and their default values.

### Database variables

These environment variables are used to configure the connection to the database. While they have default values, in case no value is given to the environment variable, it is highly recommended to set these variables when used in a production setup.

| Variable name | Description | Default Value |
| -------------- | --------------- | --------------- |
| DATABASE_USERNAME | The username for the database | postgres |
| DATABASE_PASSWORD | The password for the database | postgres |
| DATABASE_ENGINE | The engine for the database | sqlite3 |
| DATABASE_NAME | The name of the database | default_db |
| DATABASE_HOST | The host address of the database | 127.0.0.1 |
| DATABASE_PORT | The host port of the database | 5432 |

### App variables

#### Prod container

These environment variables are used to configure the app container. While they have default values, in case no value is given to the environment variable, it is highly recommended to set these variables when used in a production setup.

| Variable name | Description | Default Value |
| -------------- | --------------- | --------------- |
| DEBUG | Whether or not the project is in debug mode | 0 |
| DJANGO_SECRET_KEY | The secret key for the django project | super duper secret |
| DJANGO_ALLOWED_HOSTS | Comma-separated list of allowed host addresses | 127.0.0.1 |

#### Dev container

The dev container uses the same variables as the prod container, as well as the following.

| Variable name | Description | Default Value |
| -------------- | --------------- | --------------- |
| DEV_TEST_DATA_PROVISION | Whether the dev container should import test data on startup. Only happens once. | 1 |

### Example .env file contents

#### With postgres db

```
DATABASE_NAME=default_db
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=postgres
DATABASE_ENGINE=postgresql
DATABASE_HOST=db
DATABASE_PORT=5432

DJANGO_SECRET_KEY=super duper secret key
DJANGO_ALLOWED_HOSTS=127.0.0.1

DEBUG=0
DEV_TEST_DATA_PROVISION=1
```

## Building and publish the prod image

TODO: Info here should be updated when we have the real docker repository.

### Building image

To build the prod image run

```
docker build -t <USERNAME>/<IMAGE NAME>:<TAG NAME> .
```

Example:

```
docker build -t zargess/fellowship_bookclub:latest .
```

### Publish image

To publish the image run

```
docker publish <USERNAME>/<IMAGE NAME>:<TAG NAME>
```

Example:

```
docker publish zargess/fellowship_bookclub:latest
```

## Importing test data fixture

In the `data/` folder, there is a fixture containing a few users related to a club. This data is automatically imported in the dev app container (unless disabled). If it's disabled or the data is needed in the prod container then the following command imports the same data.

```bash
docker compose exec fellowship_app python3 manage.py loaddata data/fellowship.json
```

After this, you can log in with the username "gandalf" and the password "admin".
