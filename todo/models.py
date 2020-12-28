from django.db import models
from django.db.models import *
from django.contrib.auth.models import User

class Todo(Model):
    title = CharField(max_length=120)
    memo = TextField(blank=True)
    important = BooleanField(default=False)
    createDate = DateTimeField(auto_now_add=True)
    compliteDate = DateTimeField(blank=True, null=True)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.title
