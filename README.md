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

127.0.0.1
Here you can read about the environment variables used by the docker container and their default values.

### Database variables

These environment variables are used to configure the connection to the database. While they have default values, in case no value is given to the environment variable, it is highly recommended to set these variables when used in a production setup.

| Variable name | Description | Default Value |
| -------------- | --------------- | --------------- |
| DATABASE_USER | The username for the database | postgres |
| DATABASE_PASSWORD | The password for the database | postgres |
| DATABASE_ENGINE | The engine for the database | sqlite3 |
| DATABASE_NAME | The name of the database | default_db |
| DATABASE_HOST | The host address of the database | 127.0.0.1 |
| DATABASE_PORT | The host port of the database | 5432 |
| DJANGO_SECRET_KEY | The secret key for the django project | super duper secret |
| DEBUG | Whether or not the project is in debug mode | 0 |
| DJANGO_ALLOWED_HOSTS | Comma-separated list of allowed host addresses | 127.0.0.1 |

### Example .env file contents

#### With postgres db

```
DATABASE_NAME=default_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_ENGINE=postgresql
DATABASE_HOST=db
DATABASE_PORT=5432

DJANGO_SECRET_KEY=super duper secret key
DJANGO_ALLOWED_HOSTS=127.0.0.1

DEBUG=0
```

## Importing test data fixture

In the `data/` folder, there is a fixture containing a few users related to a club. You can import this data to the database using

```bash
docker compose exec fellowship_app python3 manage.py loaddata data/fellowship.json
```

After this, you can log in with the username "gandalf" and the password "admin".
