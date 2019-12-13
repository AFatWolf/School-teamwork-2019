from django.db import models
#from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User as AuthUser

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=256)
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

class Attend(models.Model):
    pass

class Host(models.Model):
    pass

class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=1024)
    detail = models.TextField()
    # the time event happens
    hosted_at = models.DateTimeField(default=timezone.now())
    # the time event is created
    created_at = models.DateTimeField(default=timezone.now())
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.TextField()
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    date = models.DateTimeField()
    # author
    # ForeginKey for Event
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(AuthUser, related_name='comments', on_delete=models.CASCADE, default=1)





