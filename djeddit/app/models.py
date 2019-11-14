from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.CharField(max_length = 200,blank = True)
    username = models.CharField(max_length = 20, blank = False)
    email = models.EmailField()
    karma = models.IntegerField(default = 0)
    password = models.CharField(max_length = 20)
    created_on = models.DateField(auto_now_add = True)

class Sub(models.Model):
    name = models.CharField(max_length = 30)
    created_on = models.DateField(auto_now_add = True)
    posts = models.ForeignKey(Post,on_delete = models.CASCADE)
    members = models.ManyToManyField(UserProfile)
         
class Post(models.Model):
    title = models.TextField(max_length = 50)
    content = models.TextField()
    created_by = models.OneToOneField(UserProfile,on_delete = models.CASCADE)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
    sub_posted_on = models.OneToOneField(Sub)
    created_on = models.DateField(auto_now_add = True)

class Comment(models.Model):
    parent_post = models.ForeignKey(Post, null = False)
    created_by = models.OneToOneField(UserProfile,on_delete = models.CASCADE)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add = True)

class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null = True)
    comment = models.ForeignKey(Comment,  on_delete = models.CASCADE, null = True)
    voted = models.BooleanField()
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = False)
    