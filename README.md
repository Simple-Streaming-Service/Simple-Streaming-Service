# Video Service

## Description
...

## Installation
Before running the application, you need to install the following dependencies:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

And then create a `.env` file in the root directory of the project with the following content:
```shell
# Database
MONGO_USERNAME=root
MONGO_PASSWORD=root
# Video Service
API_HOST=http://localhost:9997
LIVE_HOST=http://localhost:8888
```
And then run the following command:
```shell
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 3650 -nodes -subj '/CN=issuer'
```
And then run the following command:
```shell
docker-compose up --build -d
```

## Usage
...