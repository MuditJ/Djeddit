from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import app.models as models
import app.forms as forms
# Create your views here.

def index(request):
    return render(request,'base.html')
    #return HttpResponse('Hello World. This is the home page.')
    
def home(request):
    #After logging outvia logout_view, the user is the AnonymousUser
    return render(request, 'home.html', {'user': request.user})

def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
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

def logout_view(request):
    #Logout the current user i.e. flush user related session data
    if request.user.is_authenticated:
        logout(request)
        print(f'User now is {request.user}')
        return HttpResponse('Logged out')
    else:
        return HttpResponse(f'Nobody currently logged in')

def signup_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        else:
            form = forms.UserForm()
            return render(request,'signUp.html',{'form':form})
    elif request.method == 'POST':
        submitted_form = forms.UserForm(request.POST)
        if submitted_form.is_valid():
            new_user = submitted_form.save()
            #new_user_profile = models.UserProfile(user = new_user)
            #new_user_profile.save()
            print(f'Succesfully created new user: {new_user} who has profile: {new_user.user_profile}!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('signup')) 


def create_sub_view(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = forms.SubForm()
            return render(request,'login.html',{'form' : form})
        elif request.method == 'POST':
            submitted_form = forms.SubForm(request.POST)
            if submitted_form.is_valid():
                new_sub = submitted_form.save(commit = False) #Hold off on saving this to the database
                new_sub.created_by = request.user.user_profile
                new_sub.save()
                #No need to use the save_m2m as no many to many relationship data comes from the form
                print('Succesfully created new sub!')
                return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('home'))

def create_post_view(request):
    if request.user.is_authenticated:
        pass
    else:
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

def profile_dashboard_view(request):
    if request.user.is_authenticated:
        return HttpResponse('Yet to implement')
    else:
        return HttpResponseRedirect(reverse('home'))

def all_subs_view(request):
    subs = models.Sub.objects.all()
    return render(request,'allSubs.html',{'subs':subs})

def rising_subs_view(request):
    subs = models.Sub.objects.all()
    return render(request,'allSubs.html',{'subs' : subs})

def get_posts_for_sub(request,sub_id):
    sub = models.Sub.objects.get(pk = sub_id)
    posts = models.Post.objects.filter(sub_posted_on__pk = sub_id)
    return render(request,'posts.html',{'sub' : sub, 'posts' : posts})

def get_comments_for_post(request,post_id):
    post = models.Post.objects.get(pk = post_id)
    sub = post.sub_posted_on
    comments = post.comments.all()
    return render(request,'comments.html',{'sub' : sub, 'post': post, 'comments' : comments})

def random_view(request, num = None):
    print(request.GET)
    print(num)
    return HttpResponse('Hello')

