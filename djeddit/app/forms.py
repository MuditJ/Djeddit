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

    #Overriding save to also create a UserProfile model instance
    def save(self, *args,**kwargs):
        super().save(*args,**kwargs)
        UserProfile.objects.create(user = self)

class UserLoginForm(forms.Form):
    username = forms.CharField(label = 'Enter username:')
    password = forms.CharField(widget = forms.PasswordInput())
    

class SubForm(ModelForm):
    class Meta:
        model = Sub
        fields = ['name','description']

