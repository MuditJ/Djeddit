from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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
        return f'{self.user.username}'

class Sub(models.Model):
    name = models.CharField(max_length = 30,unique = True)
    created_by = models.ForeignKey(UserProfile,on_delete = models.CASCADE, null = True,related_name= 'created_subs')
    description = models.CharField(max_length = 100, default = 'A Djeddit sub')
    created_on = models.DateField(auto_now_add = True)
    #FIX THIS
    members = models.ManyToManyField(UserProfile,blank = True)
    #url = models.URLField() 


    def __str__(self):
        return f'{self.name}'

    
class Post(models.Model):
    title = models.TextField(max_length = 200)
    content = models.TextField()
    created_by = models.ForeignKey(UserProfile,related_name = 'posts_created',on_delete = models.CASCADE,null = False)
    #upvotes = models.IntegerField(blank = True,default = 0)
    #downvotes = models.IntegerField(blank = True,default = 0)
    sub_posted_on = models.ForeignKey('Sub', on_delete = models.CASCADE,related_name = 'posts')
    created_on = models.DateField(auto_now_add = True)

    def __str__(self):
        return f'{(self.title)} -> {self.sub_posted_on}'

class Comment(models.Model):
    parent_post = models.ForeignKey(Post, related_name = 'comments',on_delete = models.CASCADE, null = False)
    created_by = models.ForeignKey(UserProfile,related_name = 'comments_made', on_delete = models.CASCADE)
    content = models.TextField(default = 'Mitigating schema mistake')
    #upvotes = models.IntegerField(blank = True, default = 0)
    #downvotes = models.IntegerField(blank = True, default = 0)
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.content}'


class Vote(models.Model):
    post = models.ForeignKey(Post, related_name = 'votes', on_delete = models.CASCADE, blank = True, null = True)
    comment = models.ForeignKey(Comment, related_name = 'votes', on_delete = models.CASCADE, blank = True, null = True)
    voted = models.BooleanField()
    user_voted = models.ForeignKey(UserProfile, related_name = 'votes_done',on_delete = models.CASCADE, null = False)
    
    def __str__(self):
        return f'Vote made by {self.user_voted.user.username} on {self.post if not None else self.comment}'
