from django import forms
from django.forms.models import ModelForm
from app.models import UserProfile,Post,Sub,Comment
from django.contrib.auth.models import User

#Create a form for login
''' Instantiates a User model object and 
also a UserProfile model object, linking to the user'''
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password','email']
        widgets = {
            'password' : forms.PasswordInput(),
        }
    def save(self, commit=True):
        new_user = super().save(commit=False)
        new_user.set_password(self.cleaned_data["password"])
        new_user.save()
        user_profile = UserProfile(user = new_user)
        user_profile.save()
        return new_user

class UserLoginForm(forms.Form):
    username = forms.CharField(label = 'Enter username:')
    password = forms.CharField(widget = forms.PasswordInput())
    

class SubForm(ModelForm):
    class Meta:
        model = Sub
        fields = ['name','description']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','sub_posted_on']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['parent_post','content']