# EVOX

REST API written in the FastAPI framework for message persistence with authentication built-in.

### Requirements:
- Docker
- docker-compose

### Framework used
This app is built using FastAPI framework [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com).

It consists of the Starlette ASGI framework and Pydantic library.

### Running the app

Because this app requires a PostgreSQL database instance running alongside, the easiest way to run it is to use docker-compose.

``` shell
docker-compose up
```

This docker-compose config uses volumes for PostgreSQL container, so it should retain data between restarts.

### Running unit and integration tests

The following script will run tests in an isolated docker environment, so you don't have to set up a database yourself.
``` shell
./scripts/test-docker.sh
```

## API

### Endpoints list

| HTTP method   | Authentication required   | Path                      | Description             | Possible HTTP codes
| ------------- | -------------             | -------------             | -------------           | -------------
| GET           | NO                        | `/api/v1/messages/{id}`   | Get message by id       | 200, 400, 401, 404
| POST          | YES                       | `/api/v1/messages`        | Create new message      | 200, 400, 401
| PUT           | YES                       | `/api/v1/messages/{id}`   | Update existing message | 200, 400, 401, 404
| DELETE        | YES                       | `/api/v1/messages/{id}`  | Delete message          | 200, 400, 401, 404


### REST API Documentation using swagger:
[https://evox.rasztabiga.me/docs](https://evox.rasztabiga.me/docs)

It also allows users to test the API using a simple interface.

### REST API Documentation using redoc:
[https://evox.rasztabiga.me/redoc](https://evox.rasztabiga.me/redoc)

Both documentations include examples of request and response bodies. 

## Implementation details

### Data format

This REST API uses JSON data type for request and response bodies.

Example of request body:
```json
{
    "content": "New message"
}
```

Example of response body:
```json
{
    "content": "New content",
    "views_count": 5,
    "id": 3
}
```

### Persistence

Persistence is provided by SQLAlchemy ORM library and PostgreSQL database.

For SQL migrations I'm using Alembic. They are located under `alembic` directory.

### Authentication
##### API Key required to call protected endpoints:
```
HTTP Header:
Authorization: ca9c1d4509ec6c9b9550fecfab3817a9b87e5e06bcbfe94298b12ce14ca8e428
```
This key works for `evox.rasztabiga.me` server. It's being set by environmental variable passed to docker container running the app.

### Unit and integration tests

This API is covered with both unit and integration tests.

Unit tests are testing message service and cover mostly business logic. They are executed by the pytest library.

Integration tests are executed with FastAPI test HTTP client and call API endpoints, verifying their correctness.

### Deployment

This app is deployed on my private Kubernetes cluster. Configuration used for the deployment is located in the `k8s` directory.

Currently, it's running 3 replicas of backend pods, so it's easily scalable.

App is listening on the following URL: [https://evox.rasztabiga.me/api/v1/messages](https://evox.rasztabiga.me/api/v1/messages)

SSL certificate and DDoS protection is provided by Cloudflare.

### CI / CD

I'm using GitHub Actions job to execute linter and tests on each push to GitHub. It also builds and pushes Docker image of the app to DockerHub.

You can locate it here: [https://hub.docker.com/r/navareth/evox](https://hub.docker.com/r/navareth/evox)

### Environment variables

This app uses the following environment variables:

* API_KEY - API key used to authenticate requests
* POSTGRES_SERVER - hostname of PostgreSQL database
* POSTGRES_USER - username for PostgreSQL database
* POSTGRES_PASSWORD - password for PostgreSQL database
* POSTGRES_DB - database name for PostgreSQL database
* BACKEND_CORS_ORIGINS - allowed origins for CORS mechanism

## API usage

Following examples use the demo server `https://evox.rasztabiga.me`

`API_KEY=ca9c1d4509ec6c9b9550fecfab3817a9b87e5e06bcbfe94298b12ce14ca8e428`

You will have to replace `MESSAGE_ID` placeholder if you want to run these examples by yourself.

### Create message

```sh
curl --location --request POST 'https://evox.rasztabiga.me/api/v1/messages' \
--header 'Authorization: ca9c1d4509ec6c9b9550fecfab3817a9b87e5e06bcbfe94298b12ce14ca8e428' \
--header 'Content-Type: application/json' \
--data-raw '{
    "content": "New message"
}'
```

### View message

```sh
curl --location --request GET 'https://evox.rasztabiga.me/api/v1/messages/{MESSAGE_ID}'
```

### Update message

```sh
curl --location --request PUT 'https://evox.rasztabiga.me/api/v1/messages/{MESSAGE_ID}' \
--header 'Authorization: ca9c1d4509ec6c9b9550fecfab3817a9b87e5e06bcbfe94298b12ce14ca8e428' \
--header 'Content-Type: application/json' \
--data-raw '{
    "content": "New content"
}'
```

### Delete message

```sh
curl --location --request DELETE 'https://evox.rasztabiga.me/api/v1/messages/{MESSAGE_ID}' \
--header 'Authorization: ca9c1d4509ec6c9b9550fecfab3817a9b87e5e06bcbfe94298b12ce14ca8e428'
```