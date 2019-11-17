from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import app.models as models
import app.forms as forms
# Create your views here.

def index(request):
    return HttpResponse('Hello World. This is the home page.')
    
def home(request):
    #After logging outvia logout_view, the user is the AnonymousUser
    return HttpResponse(f'This is the home page. Current user is {request.user}')

def logout_view(request):
    #Logout the current user i.e. flush user related session data
    if request.user.is_authenticated:
        logout(request)
        print(f'User now is {request.user}')
        return HttpResponse('Logged out')
    else:
        return HttpResponse(f'Nobody currently logged in')

def login_view(request):
    if request.method == 'GET':
        form = forms.UserLoginForm()
        return render(request,'login.html',{'form' : form})
    elif request.method == 'POST':
        print('Processing login request')
        submitted_form = forms.UserLoginForm(request.POST)
        print(hasattr(submitted_form,'cleaned_data')) #False
        if submitted_form.is_valid():
            print(hasattr(submitted_form,'cleaned_data')) #True
            print(submitted_form.cleaned_data) #Data which passes the validation stage
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username = username, password = password)
            if user is not None:
                login(request,user)
                print('Succesfully logged in!')
            else:
                print('No such user exists.Try again')
            return HttpResponseRedirect(reverse('home'))
        else:
            print('Something went wrong')
            return HttpResponseRedirect(reverse('home'))

def create_sub_view(request):
    if request.method == 'GET':
        form = forms.SubForm()
        return render(request,'login.html',{'form' : form})
    elif request.method == 'POST':
        submitted_form = forms.SubForm(request.POST)
        if submitted_form.is_valid():
            submitted_form.save()
            print('Succesfully created new sub!')
            return HttpResponseRedirect(reverse('home'))


def profile_view(request):
    if request.user.is_authenticated:
        user = request.user.user_profile
        subs = user.sub_set
        posts = user.post_set
        comments = user.comment_set
        return render(request,'profile.html',{'subs':subs,'comments' : comments, 'posts':posts})
    else:
        return HttpResponse('You need to log in first')

def all_subs_view(request):
    subs = models.Sub.objects.all()
    return render(request,'allSubs.html',{'subs':subs})
