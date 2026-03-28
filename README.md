# Fantasy Fellowship Book Club Application

A simple Node Express app in docker.

## How to

To run the application locally, simply run

```
docker compose up -d
```

and navigate to `localhost:3000`.

## Environment variables

| Variable name | Description | Default Value |
| -------------- | --------------- | --------------- |
| DB_USER | The username for the database | postgres |
| DB_PASSWORD | The password for the database | postgres |
| DB_SCHEMA | The name of the DB schema | postgres |
| DB_HOST | The hostname of the database | postgres |

