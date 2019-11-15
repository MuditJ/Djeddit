from django.db import models
from django.contrib.auth.models import User

# Create your models here.

DEFAULT_USER = User.objects.first() #Mudit-Admin

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, related_name= 'user_profile')
    bio = models.CharField(max_length = 200,blank = True)
    #These fields are present in the User model
    #username = models.CharField(max_length = 20, blank = False)
    #email = models.EmailField()
    #password = models.CharField(max_length = 20)    
    karma = models.IntegerField(default = 0)
    created_on = models.DateField(auto_now_add = True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

class Sub(models.Model):
    name = models.CharField(max_length = 30,unique = True)
    created_by = models.ForeignKey(User,on_delete = models.CASCADE, null = True)
    description = models.CharField(max_length = 100, default = 'A Djeddit sub')
    created_on = models.DateField(auto_now_add = True)
    #FIX THIS
    members = models.ManyToManyField(UserProfile,blank = True)

    def __str__(self):
        return f'{self.name}'

    
class Post(models.Model):
    title = models.TextField(max_length = 50)
    content = models.TextField()
    created_by = models.ForeignKey(UserProfile,on_delete = models.CASCADE,null = False)
    upvotes = models.IntegerField(blank = True,default = 0)
    downvotes = models.IntegerField(blank = True,default = 0)
    sub_posted_on = models.ForeignKey('Sub', on_delete = models.CASCADE)
    created_on = models.DateField(auto_now_add = True)

    def __str__(self):
        return f'{(self.title)} -> {self.sub_posted_on}'

class Comment(models.Model):
    parent_post = models.ForeignKey(Post, on_delete = models.CASCADE, null = False)
    created_by = models.ForeignKey(UserProfile,on_delete = models.CASCADE)
    content = models.TextField(default = 'Mitigating schema mistake')
    upvotes = models.IntegerField(blank = True, default = 0)
    downvotes = models.IntegerField(blank = True, default = 0)
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.content[:20]}'

class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null = True)
    comment = models.ForeignKey(Comment,  on_delete = models.CASCADE, null = True)
    voted = models.BooleanField()
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null = False)
    