import os
from flask import Flask
from microkubes.gateway import KongGatewayRegistrator
from db import DB
from flask import request
import json
# from microkubes.security import FlaskSecurity
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

registrator = KongGatewayRegistrator(os.environ.get("API_GATEWAY_URL", "http://localhost:8001"))  # Use the Kong registrator for Microkubes

# set up a security chain
# sec = (FlaskSecurity().
#         keys_dir("./keys").   # set up a key-store that has at least the public keys from the platform
#         jwt().                # Add JWT support
#         oauth2().             # Add OAuth2 support
#         build())              # Build the security for Flask

# Self-registration on the API Gateway must be the first thing we do when running this service.
# If the registration fails, then the whole service must terminate.
registrator.register(name="microservice-python-example",                  # the service name.
                     paths=["/todos"],                      # URL pattern that Kong will use to redirect requests to out service
                     host="microservice-python-example.services.consul",  # The hostname of the service.
                     port=5000)                             # Flask default port. When redirecting, Kong will call us on this port.

db = DB()
 
@app.route("/todos", methods=["GET"])
def todos():
    """
    This is the todo listing API.
    Call this api passing a limit and get back all the todos in the limit range.
    ---
    parameters:
      - name: limit
        in: query
        type: integer
        required: false
        description: The number of Todos to return
    definitions:
        Todo:
            type: object
            properties:
                _id:
                    type: object
                    properties:
                        $oid:
                            type: string
                title:
                    type: string
                    description: Todo title
                description:
                    type: string
                    description: Todo description
                done:
                    type: boolean
                    description: Shows if the todo is completed or not.
                createdAt:
                    type: object
                    properties:
                        $date:
                            type: integer
                completedAt:
                    type: object
                    properties:
                        $date:
                            type: integer
        Todos:
            type: array
            items:
                $ref: '#/definitions/Todo'
    responses:
        400:
            description: Input validation error.
        200:
            description: All todos have been listed.
            schema:
                $ref: '#/definitions/Todos'
            examples:
                [
                    {
                        "_id": {
                            "$oid": "5be9d46127ad405ec67488c9"
                        },
                        "title": "Title 1",
                        "description": "Description 1",
                        "done": true,
                        "createdAt": {
                            "$date": 1542054513199
                        },
                        "completedAt": {
                            "$date": 1542206121677
                        }
                    },
                    {
                        "_id": {
                            "$oid": "5be9d46a27ad405ec67488ca"
                        },
                        "title": "Title 2",
                        "description": "Description 2",
                        "done": false,
                        "createdAt": {
                            "$date": 1542054522470
                        }
                    }
                ]
    """
    if request.args.get("limit") is not None: 
        limitTodos = int(request.args.get("limit"))
    else:
        limitTodos = 10
    listTodos = db.getAllTodos(limit=limitTodos)
    return listTodos

@app.route("/todos", methods=["POST"])
def createTodo():
    """
    This is the API for creating todos.
    ---
    summary: Creates a new user.
    consumes:
        - application/json
    parameters:
          - in: body
            name: todo
            description: The todo to create.
            schema:
                type: object
                required:
                    -title
                    -description
                properties:
                    title:
                        type: string
                    description:
                        type: string
    responses:
        400:
            description: The title and/or description are not provided.
        200:
            description: New Todo was successfully created.
            schema:
                $ref: '#/definitions/Todo'
            examples:
                {
                    "_id": {
                        "$oid": "5be9d46127ad405ec67488c9"
                    },
                    "title": "Title 1",
                    "description": "Description 1",
                    "done": true,
                    "createdAt": {
                        "$date": 1542054513199
                    },
                }
    """
    payload = request.get_json()
    newTodo = db.createTodo(payload)
    return newTodo

@app.route("/todos/<todoId>", methods=["GET"])
def getTodoById(todoId):
    """
    This is the todo listing API using the todo ID.
    Call this api passing a todoId and get back the todo to with the ID that was provided..
    ---
    parameters:
      - name: todoId
        in: path
        type: string
        required: true
        description: The id of the Todo
    definitions:
        Todo:
            type: object
            properties:
                _id:
                    type: object
                    properties:
                        $oid:
                            type: string
                title:
                    type: string
                    description: Todo title
                description:
                    type: string
                    description: Todo description
                done:
                    type: boolean
                    description: Shows if the todo is completed or not.
                createdAt:
                    type: object
                    properties:
                        $date: 
                            type: integer
                completedAt:
                    type: object
                    properties:
                        $date:
                            type: integer
    responses:
        400:
            description: Todo matching query does not exist.
        200:
            description: The todo is listed.
            schema:
                $ref: '#/definitions/Todo'
            examples:
                {
                    "_id": {
                        "$oid": "5be9d46127ad405ec67488c9"
                    },
                    "title": "Title 1",
                    "description": "Description 1",
                    "done": true,
                    "createdAt": {
                        "$date": 1542054513199
                    },
                }
    """

    existingTodo = db.getTodoById(todoId)
    return existingTodo

@app.route("/todos/<todoId>", methods=["DELETE"])
def deleteTodo(todoId):
    """
    This is the todo deleting API.
    Call this api passing a todoId and delete the todo with the provided id.
    ---
    parameters:
      - name: todoId
        in: path
        type: string
        required: true
        description: The id of the Todo
    definitions:
        Todo:
            type: object
            properties:
                _id:
                    type: object
                    properties:
                        $oid:
                            type: string
                title:
                    type: string
                    description: Todo title
                description:
                    type: string
                    description: Todo description
                done:
                    type: boolean
                    description: Shows if the todo is completed or not.
                createdAt:
                    type: object
                    properties:
                        $date:
                            type: integer
                completedAt:
                    type: object
                    properties:
                        $date:
                            type: integer
    responses:
        400:
            description: Todo matching query does not exist.
        200:
            description: The todo has been deleted.
            schema:
                properties:
                    msg:
                        type: string
                        description: This field will display a message that the todo has been deleted.
    """
    deletedTodo = db.deleteTodo(todoId)
    return deletedTodo

@app.route("/todos/<todoId>", methods=["PUT", "PATCH"])
def updateTodo(todoId):
    """
    This is the todo updating API using the todo ID.
    Call this api passing a todoId and get back an updated todo.
    ---
    parameters:
      - name: todoId
        in: path
        type: string
        required: true
        description: The id of the Todo
      - name: updated todo info
        in: body
        description: The updated todo information.
        schema:
            type: object
            properties:
                title:
                    type: string
                description:
                    type: string
                done:
                    type: boolean
    definitions:
        Todo:
            type: object
            properties:
                _id:
                    type: object
                    properties:
                        $oid:
                            type: string
                title:
                    type: string
                    description: Todo title
                description:
                    type: string
                    description: Todo description
                done:
                    type: boolean
                    description: Shows if the todo is completed or not.
                createdAt:
                    type: object
                    properties:
                        $date:
                            type: integer
                completedAt:
                    type: object
                    properties:
                        $date:
                            type: integer
    responses:
        400:
            description: Todo matching query does not exist.
        200:
            description: The todo is updated.
            schema:
                $ref: '#/definitions/Todo'
            examples:
                {
                    "_id": {
                        "$oid": "5be9d46127ad405ec67488c9"
                    },
                    "title": "Title 1",
                    "description": "Description 1",
                    "done": true,
                    "createdAt": {
                        "$date": 1542054513199
                    },
                }
    """
    payload = request.get_json()
    updatedTodo = db.updateTodo(todoId, payload)
    return updatedTodo