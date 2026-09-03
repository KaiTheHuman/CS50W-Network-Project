from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)
    likes_users = models.ManyToManyField(User, related_name="likes", blank=True)

