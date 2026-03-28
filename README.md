# Fantasy Fellowship Book Club Application

A simple Node Express app in docker.

## How to

To run the application locally, simply run

```
docker compose up -d
```

and navigate to `localhost:3000`.

## Environment variables

Here you can read about the environment variables used by the docker container and their default values.

### Database variables

These environment variables are used to configure the connection to the database. While they have default values, in case no value is given to the environment variable, it is highly recommended to set these variables when used in a production setup.

| Variable name | Description | Default Value |
| -------------- | --------------- | --------------- |
| DB_USER | The username for the database | postgres |
| DB_PASSWORD | The password for the database | postgres |
| DB_SCHEMA | The name of the DB schema | postgres |
| DB_HOST | The hostname of the database | postgres |

