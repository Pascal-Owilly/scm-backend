# models.py
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class CustomUser(AbstractUser):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    id_number = models.PositiveIntegerField(default=0)
    email = models.EmailField(unique=True)
    market = models.CharField(max_length=100)
    community = models.CharField(max_length=100)
    head_of_family = models.BooleanField(default=False)
    country = models.CharField(max_length=50)
    groups = models.ManyToManyField(Group, related_name='users', blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username + ' Profile'