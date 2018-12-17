### Introduction

This is an example of a microservice for managing todos written in Python using Flask. Its purpose is to showcase how to use it within the Microkubes platform. It contains documentation on how to setup and run the microservice, as well as explanation of the steps on how you can create your own microservice and deploy it into the Microkubes platform.

### Installation

First make sure that the Microkubes platform is deployed with Kubernetes and up and running. Follow the instructions [here](https://github.com/Microkubes/microkubes) on how to setup Microkubes with Kubernetes.

To install the microservice, first you have to build an image with Docker:

```
docker build -t microkubes/microservice-python-example .
```

Then, in the [microkubes](https://github.com/Microkubes/microkubes) repo, in the       [microkubes.yaml](https://github.com/Microkubes/microkubes/blob/master/kubernetes/manifests/microkubes.yaml) file,
add the following at the bottom:

```
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: microservice-python-example
  namespace: microkubes
  labels:
    app: microservice-python-example
    platform: microkubes
spec:
  replicas: 1
  template:
    metadata:
      name: microservice-python-example
      labels:
        app: microservice-python-example
        platform: microkubes
      annotations:
        consul.register/enabled: "true"
        consul.register/service.name: "microservice-python-example"
    spec:
      containers:
        - name: microservice-python-example
          image: microkubes/microservice-python-example:latest
          imagePullPolicy: Never
          env:
            - name: SERVICE_CONFIG_FILE
              value: /config.json
            - name: API_GATEWAY_URL
              value: "http://kong-admin:8001"
          ports:
            - containerPort: 5000
          volumeMounts:
            - name: microkubes-secrets
              mountPath: /run/secrets
      volumes:
        - name: microkubes-secrets
          secret:
            secretName: microkubes-secrets
```

After that, in [.env](https://github.com/Microkubes/microkubes/blob/master/kubernetes/manifests/mongo/.env) add the following environment variables for Mongo database:

```
MS_TODO_DB=todos
MS_TODO_USER=restapi
MS_TODO_PWD=restapi
```

Next, in [create_microkubes_db_objects.sh](https://github.com/Microkubes/microkubes/blob/master/kubernetes/manifests/mongo/create_microkubes_db_objects.sh) add the following line at the end to create the database for todos:

```
mongo  -u admin -p admin --authenticationDatabase admin "$MS_TODO_DB" --eval "db.createUser({user: '$MS_TODO_USER', pwd: '$MS_TODO_PWD', roles: [{role: 'dbOwner', db: '$MS_TODO_DB'}]});"
```

Next thing to do is to update [values.yaml] (https://github.com/Microkubes/microkubes/blob/master/kubernetes/helm/microkubes/values.yaml).
Add the following code right after the declared variable for `User profile`:

```
# Microkubes Python example
  microservicepythonexample:
    name: microservice-python-example
    serviceConfigPath: /etc/config/config.json

  image:
    repository: microkubes/microservice-python-example
    tag: latest
    pullPolicy: Never

  podAnnotations:
    consul.register/enabled: "true"
    consul.register/service.name: "microservice-python-example"
```

Finally, redeploy the Microkubes stack with Kubernetes and check if the service is running using `kubectl -n microkubes get pods`.

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

Prior running the tests, make sure that you have a running MongoDB instance on localhost:27017.
To run the tests type `DB_NAME="todos_test" FLASK_ENV="testing" python test_service.py`.

## Contributing

 For contributing to this repository or its documentation, see the [Contributing guidelines](CONTRIBUTING.md).