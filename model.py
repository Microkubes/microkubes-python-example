from mongoengine import *
import datetime


class Todo(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    done = BooleanField(required=True, default=False)
    createdAt = DateTimeField(default=datetime.datetime.now)
    completedAt = DateTimeField()
    createdBy = StringField()