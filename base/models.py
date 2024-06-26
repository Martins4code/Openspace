from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    
    avatar= models.ImageField(null=True, default="avatar.svg")
    
    USERNAME_FIELD = 'email' #the username field is now email 
    REQUIRED_FIELDS = []



class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Space(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
     
     
    class Meta():
       ordering  = ['-updated', '-created']  # ordering is based on date/time created or updated
    
    
    def __str__(self):  # created string representation of our space
        return self.name
    # we have a many to one relationship where a single space contains multiple messages
    
    # note message is a child of User and Space ps it exists within them ps we can have multi message but one user and space.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)# we establish a relationship btw the Space and Messages model here and the cascade means that when the room is deleted all messages contained inside are also deleted 
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta():
       ordering  = ['-updated', '-created']
    
    def __str__(self):  # created string representation of our body we want the first 50 charactes as our preview 
        return self.body[0:50]
    

    