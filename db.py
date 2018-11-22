from mongoengine import *
from model import Todo
import json
import datetime
import os


class DB:
    def __init__(self):
        db_name = os.environ.get("DB_NAME", "todos")
        connect(db_name, host="mongo", port=27017, username="admin", password="admin", authentication_source="admin")

    def createTodo(self, payload):
        newTodo = Todo(
            title=payload.get("title"),
            description=payload.get("description")
        )
        try:
            newTodo.save()
        except ValidationError as error:
            errorMessage = {
                "msg": str(error)
            }
            return json.dumps(errorMessage)
            
        return newTodo.to_json()

    def getAllTodos(self, limit=10):
        listTodos = Todo.objects[:limit]
        return listTodos.to_json()

    def getTodoById(self, todoId):
        try:
            extistingTodo = Todo.objects.get(id=todoId)
        except Todo.DoesNotExist as error:
            errorMessage = {
                "msg": str(error)
            }
            return json.dumps(errorMessage)
        return extistingTodo.to_json()

    def deleteTodo(self, todoId):
        try:
            deletedTodo = Todo.objects.get(id=todoId)
        except Todo.DoesNotExist as error:
            errorMessage = {
                "msg": str(error)
            }
            return json.dumps(errorMessage)

        deletedTodoTitle = deletedTodo.title
        try:
            deletedTodo.delete()
        except Todo.DoesNotExist as error:
            errorMessage = {
                "msg": str(error)
            }
            return json.dumps(errorMessage)
        
        message = {
            "msg": "The todo with title: {0} is now deleted".format(deletedTodoTitle)
        }
        return json.dumps(message)

    def updateTodo(self, todoId, payload):
        try:
            updateTodo = Todo.objects.get(id=todoId)
        except Todo.DoesNotExist as error:
            errorMessage = {
                "msg": str(error)
            }
            return json.dumps(errorMessage)

        if payload.get("title") is not None:
            updateTodo.title = payload.get("title")
        if payload.get("description") is not None:
            updateTodo.description = payload.get("description")
        if payload.get("done") is not None:
            updateTodo.done = payload.get("done")
            if updateTodo.done is True:
                updateTodo.completedAt = datetime.datetime.now()

        updateTodo.save()

        return updateTodo.to_json()