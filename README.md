# Fantasy Fellowship Book Club Application

A simple django app in docker.

## Required software for local development

* Docker with docker compose ([official installation guide](https://docs.docker.com/engine/install/))
* uv - a python pacakge and project manager ([official installation guide](https://docs.astral.sh/uv/getting-started/installation))
  * pipx is a good solution

## How to

### Development

To run the application locally, simply run

```bash
docker compose up -d
```

and navigate to `localhost:8000`.

If you have not run the application before, you may need to build it first:

```bash
docker compose build
```

and then migrate after the containers are up:

```bash
docker compose exec fellowship_app python3 manage.py migrate
```

#### Locally installed dependencies

If you want to install python dependencies locally (for the sake of your IDE for example).

```bash
uv sync
```

#### Translations

Compiling translations at runtime is a pain in the ass, so please do this yourself:

```bash
uv run manage.py compilemessages
```

## Installing new dependencies
This gives you a virtual environment with the correct python version and all dependencies installed.

### Installing new dependencies

This project uses uv to manage dependencies and has a split in normal and dev dependencies. uv has been configured to not install or upgrade to versions of dependencies newer than 7 days. This is to help reduce the risk of being affected by a supply-chain attack. Malware scanning has also been enabled to try and detect if there are issues. This is an experimental feature and only detects packages that are already known to be malware.

[Read more on managing dependencies with uv](https://docs.astral.sh/uv/concepts/projects/dependencies/)

#### Install new prod dependency

To install a new prod dependency you should run the following command:

```bash
uv add <DEPENDENCY NAME>
```

Example:

```bash
uv add django
```

#### Install dev dependency

If a dependency is needed for development/test only then those can be installed as follows:

```bash
uv add --dev <DEPENDENCY NAME>
```

Example:

```bash
uv add --dev pytest
```

These dependencies will be installed locally and inside the dev version of the container, but not in the production container.

#### Upgrade dependencies

[Read more on upgrading dependencies here](https://docs.astral.sh/uv/concepts/projects/sync/#upgrading-locked-package-versions)

##### Upgrade explicit dependency

We have dependencies defined inside pyproject.toml. To upgrade those, you should change the version number and then run:

```bash
uv lock && uv sync
```

This will update the dependency and sync it to your machine.

##### Upgrade all dependencies

To upgrade all dependencies run

```bash
uv lock --upgrade && uv sync
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

### Building image

To build the prod image run

```
docker build -t draagdunk/fellowship_app:<TAG NAME> .
```

Example:

```
docker build -t draagdunk/fellowship_app:latest .
```

### Publish image

To publish the image run

```
docker push draagdunk/fellowship_app:<TAG NAME>
```

Example:

```
docker push draagdunk/fellowship_app:latest
```

## Importing test data fixture

In the `data/` folder, there is a fixture containing a few users related to a club. This data is automatically imported in the dev app container (unless disabled). If it's disabled or the data is needed in the prod container then the following command imports the same data.

```bash
docker compose exec fellowship_app python3 manage.py loaddata data/fellowship.json
```

After this, you can log in with the username "gandalf" and the password "admin".
