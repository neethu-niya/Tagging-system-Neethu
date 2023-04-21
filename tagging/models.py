from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

CHOICES = (
    ("1", "like"),
    ("2", "dislike"),
    ("3", "no reaction"),
)

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def is_user_liked(self,user):
        return UserReaction.objects.filter(user=user,post=self,reaction="1").exists()
    def is_user_disliked(self,user):
        return UserReaction.objects.filter(user=user,post=self,reaction="2").exists()
    def likes(self):
        return UserReaction.objects.filter(post=self,reaction="1").count()
    def dislikes(self):
        return UserReaction.objects.filter(post=self,reaction="2").count()
    @property
    def like_count(self):
        likes=UserReaction.objects.filter(post=self,reaction="1").count()
        if not likes:
            return "0"
        return likes
    @property
    def dislike_count(self):
        dislikes=UserReaction.objects.filter(post=self,reaction="2").count()
        if not dislikes:
            return "0"
        return dislikes

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.post.title

class UserReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(
        max_length = 20,
        choices = CHOICES,
        default = '1')

    def __str__(self):
        return self.post.title

class Tag(models.Model):
    tag = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tag

class PostTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_tag")
    weight = models.IntegerField(default=0)
    def __str__(self):
        return self.post.title