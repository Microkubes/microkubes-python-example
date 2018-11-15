### Introduction

This is an example of a microservice for managing todos written in Python using Flask. Its purpose is to showcase how to use it within the Microkubes platform. It contains documentation on how to setup and run the microservice, as well as explanation of the steps on how you can create your own microservice and deploy it into the Microkubes platform.

### Installation

First make sure that the Microkubes platform is up and running. Follow the instructions [here](https://github.com/Microkubes/microkubes) on how to setup Microkubes.

To install the microservice, first you have to build an image with Docker:

```
docker build -t microkubes/microkubes-python-example .
```

Then, in the [microkubes](https://github.com/Microkubes/microkubes) repo, in the       [docker-compose.fullstack.yml](https://github.com/Microkubes/microkubes/blob/master/docker/docker-compose.fullstack.yml) file,
add the `microkubes-python-example` service:

```
microkubes-python-example:
    image: microkubes/microkubes-python-example:latest
    environment:
        - API_GATEWAY_URL=http://kong:8001
        - MONGO_URL=mongo:27017
    deploy:
        restart_policy:
            condition: on-failure
    secrets:
        - public.pub
        - service.key
        - service.cert
        - system
        - default
        - system.pub
        - default.pub
```

After that, in [.env](https://github.com/Microkubes/microkubes/blob/master/docker/.env) add the following environment variables for Mongo database:

```
MS_TODO_DB=todos
MS_TODO_USER=restapi
MS_TODO_PWD=restapi
```

Next, in [create_db_objects.sh](https://github.com/Microkubes/microkubes/blob/master/docker/mongo/create_db_objects.sh) add the following line at the end to create the database for todos:

```
mongo  -u admin -p admin --authenticationDatabase admin "$MS_TODO_DB" --eval "db.createUser({user: '$MS_TODO_USER', pwd: '$MS_TODO_PWD', roles: [{role: 'dbOwner', db: '$MS_TODO_DB'}]});"
```

Finally, redeploy the Microkubes stack and check if the service is running using `docker service ls`.

### API documentation

When the service is up and running, a Swagger documentation of the API is available at http://localhost:5000/apidocs/.

### Libraries and tools

The microkubes-python-example is built using Python, and it uses the following libraries:
- [Flask](http://flask.pocoo.org/)
- [microkubes-python](https://github.com/Microkubes/microkubes-python)
- [mongoengine](https://github.com/MongoEngine/mongoengine)

#### Flask

Flask is a microframework for Python based on Werkzeug. It allows for creating REST API services.
You can learn more about Flask and how to define the API [here](http://flask.pocoo.org/).

#### microkubes-python

`microkubes-python` is a library which provides tools and helpers for microservices written in Python on top of Microkubes. It supports registering a microservice on the Kong API gateway, security that works with Microkubes' own security and user management, support for JWT and OAuth2 based auth and an integration with Flask, so that Flask API endpoints can be secured.

#### mongoengine

MongoEngine is a Python Object-Document Mapper for working with MongoDB.

### Tests

To run the tests type `DB_NAME="todos_test" python test_service.py`.