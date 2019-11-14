from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login,logout
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
