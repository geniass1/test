from django.db import models
from user.models import NewUser
from datetime import datetime


class Friends(models.Model):
    who = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='who_likes')
    whom = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='whom_likes')
    created = models.DateField(default=datetime.now)


class Messages(models.Model):
    who = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='who_messages')
    whom = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='whom_messages')
    created = models.DateField(default=datetime.now)
    message = models.TextField()


