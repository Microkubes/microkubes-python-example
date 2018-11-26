from service import app
import unittest
import json
from mongoengine.connection import _get_db

class TestService(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.token = "Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NDMzMjc0MTUsImlhdCI6MTU0MzI0MTAxNSwiaXNzIjoiSm9ybXVuZ2FuZHIgSldUIEF1dGhvcml0eSIsImp0aSI6ImExOGEzOTQ0LWUyM2QtNDk4My1hZTYwLThlMGEyOWE0ZGM3ZSIsIm5iZiI6MCwib3JnYW5pemF0aW9ucyI6IiIsInJvbGVzIjoidXNlciIsInNjb3BlcyI6IlwiYXBpOnJlYWRcIiIsInN1YiI6IjViZmJmY2FiODJlNjIyMDAwMTJjMmM0NSIsInVzZXJJZCI6IjViZmJmY2FiODJlNjIyMDAwMTJjMmM0NSIsInVzZXJuYW1lIjoiYW5hQGFuYS5jb20ifQ.BdQB0FxEXR33Sitn__59Iii98BAbrsQay0Z-XdOH_E6OW7oyEJQc50jr63aftRP8cLqVMPXyR-_qRYbiz8Pm3kFUXGfLAY3bSRrmTPKqhCNUiLbEbm9TKcPpYJVPt0twrLtFDPv28stDPEmfI4WcowsqbVoqaAckJZsFJTpm87bRiAOuquiGMyACgcoFaTiJiSUpTUBDvnqcUCPrYvkX61Ht6gVXN7YsC952v6dWBHmQo3mKiFyBCC7JxGtcH-cojsklRzIu0G90Td6h-SdixQtZs07lrggG9T41s9rPvoeKiUc3BBN_pWweok3zpVdn89UW8CZAN_r3sAB2-camCQ"
    
    def tearDown(self):
        db = _get_db()
        db.drop_collection("todo")

    def test_createTodo(self):
        payload = {
            "title": "new title test",
            "description": "todo description test"
        }
        response = self.app.post("/todos", json=payload, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)
        assert data.get("title") == "new title test"
        assert data.get("description") == "todo description test"

    def test_createTodoError(self):
        payload = {
            "title": "new title error test"
        }
        response = self.app.post("/todos", json=payload, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)
        assert data.get("msg") == "ValidationError (Todo:None) (Field is required: ['description'])"

    def test_createTodo_noAuth(self):
        payload = {
            "title": "new title test",
            "description": "todo description test"
        }
        response = self.app.post("/todos", json=payload)
        data = json.loads(response.data)
        assert data == {'code': 401, 'message': 'authentication required'}


    def test_getAllTodos(self):
        response = self.app.get("/todos")
        data = json.loads(response.data)
        assert len(data) == 0
        for i in range(8):
            todo = {
                "title": "title1",
                "description": "descr"
            }
            self.app.post("/todos", json=todo, headers={
                "Authorization": self.token
            })
        response = self.app.get("/todos")
        data = json.loads(response.data)
        assert len(data) == 8

    def test_getTodoByID(self):
        payload = {
            "title": "title",
            "description": "descr"
        }
        response = self.app.post("/todos", json=payload, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)

        todoId = data.get("_id").get("$oid")
        response = self.app.get("/todos/{0}".format(todoId))
        data = json.loads(response.data)
        
        assert data.get("title") == "title"
        assert data.get("description") == "descr"

    def test_getTodoByIDError(self):
        payload = {
            "title": "title",
            "description": "descr"
        }
        response = self.app.post("/todos", json=payload, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)

        response = self.app.get("/todos/5be9d45627ad405ec67488c8")
        data = json.loads(response.data)
        
        assert data.get("msg") == "Todo matching query does not exist."

    def test_deleteTodo(self):
        payload = {
            "title": "title",
            "description": "descr"
        }
        
        response = self.app.post("/todos", json=payload, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)

        todoId = data.get("_id").get("$oid")
        response = self.app.delete("/todos/{0}".format(todoId), headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)
        assert data.get("msg") == "The todo with title: title is now deleted"
    
    def test_deleteTodoError(self):
        payload = {
            "title": "title",
            "description": "descr"
        }
        
        response = self.app.post("/todos", json=payload, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)

        response = self.app.delete("/todos/5be9d45627ad405ec67488c8", headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)
        assert data.get("msg") == "Todo matching query does not exist."

    def test_deleteTodo_noAuth(self):
        payload = {
            "title": "title",
            "description": "descr"
        }
        
        response = self.app.post("/todos", json=payload, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)

        todoId = data.get("_id").get("$oid")
        response = self.app.delete("/todos/{0}".format(todoId))
        data = json.loads(response.data)
        assert data == {'code': 401, 'message': 'authentication required'}
    
    def test_updateTodo(self):
        payload = {
            "title": "title",
            "description": "descr"
        }
        response = self.app.post("/todos", json=payload, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)

        todoId = data.get("_id").get("$oid")
        payloadUpdate = {
            "title": "updated Title",
            "description": "updated",
            "done": True

        }
        response = self.app.put("/todos/{0}".format(todoId), json=payloadUpdate, headers={
            "Authorization": self.token
        })

        data = json.loads(response.data)
        assert data.get("title") == "updated Title"
        assert data.get("description") == "updated"
        assert data.get("done") is True

    def test_updateTodoError(self):
        payload = {
            "title": "title",
            "description": "descr"
        }
        response = self.app.post("/todos", json=payload, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)

        payloadUpdate = {
            "title": "updated Title",
            "description": "updated",
            "done": True

        }
        response = self.app.put("/todos/5be9d45627ad405ec67488c8", json=payloadUpdate, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)
        assert data.get("msg") == "Todo matching query does not exist."
    
    def test_updateTodo_noAuth(self):
        payload = {
            "title": "title",
            "description": "descr"
        }
        response = self.app.post("/todos", json=payload, headers={
            "Authorization": self.token
        })
        data = json.loads(response.data)

        todoId = data.get("_id").get("$oid")
        payloadUpdate = {
            "title": "updated Title",
            "description": "updated",
            "done": True

        }
        response = self.app.put("/todos/{0}".format(todoId), json=payloadUpdate)

        data = json.loads(response.data)
        assert data == {'code': 401, 'message': 'authentication required'}


if __name__ == '__main__':
    unittest.main()
