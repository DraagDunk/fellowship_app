# Fantasy Fellowship Book Club Application

A simple django app in docker.

## How to

To run the application locally, simply run

```bash
docker compose up -d
```

and navigate to `localhost:8000`.

If you have not run the application before, you may need to build it first:

```bash
docker compose build
```

If you want to install python dependencies locally (for the sake) of your IDE for example), start a virtual environment before installing using pip:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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
