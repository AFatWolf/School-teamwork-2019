from django.db import models
#from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User as AuthUser
from django import forms
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
class User(AuthUser):
    # username
    # password
    # first_name
    # last_name
    description = models.TextField(default="")
    contact = models.TextField(default="")
    age = models.IntegerField(default=0)
<<<<<<< Updated upstream
=======
    first_time = models.IntegerField(default=1)
    tags = models.ManyToManyField(Tag)
>>>>>>> Stashed changes
    first_time = models.IntegerField(default=0)

class SignUpForm(UserCreationForm):
    first_name=forms.CharField(max_length=30, required=False )
    last_name=forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = AuthUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
class Attend(models.Model):
    # lists of events that you attend = slide display like homepage
    pass

class Host(models.Model):
    # lists of events that you host = this too 
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
    date = models.DateTimeField(default=timezone.now())
    # author
    # ForeginKey for Event
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(AuthUser, related_name='comments', on_delete=models.CASCADE, default=1)





