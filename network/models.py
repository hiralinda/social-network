from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from .forms import BACKGROUND_CHOICES


class User(AbstractUser):
    background_choice = models.CharField(max_length=100, choices=BACKGROUND_CHOICES, default='linear-gradient(to right, #bdc3c7, #2c3e50);')

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]} ({self.created_at})"
    
    def user_liked(self, user):
        return Like.objects.filter(post=self, user=user).exists()
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')

    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    background_choice = models.CharField(max_length=100, choices=BACKGROUND_CHOICES)

    # Add any other settings fields as needed

    def __str__(self):
        return self.user.username + "'s Settings"