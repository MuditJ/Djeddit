from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.contrib import messages 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.urls import reverse
import app.models as models
import app.forms as forms

#For sentiment analysis of all comments on a post
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Create your views here.

def index(request):
    return render(request,'base.html')
    #return HttpResponse('Hello World. This is the home page.')
    
def home(request):
    #After logging outvia logout_view, the user is the AnonymousUser
    user = request.user
    if user.is_authenticated:
        pass
        posts = models.Post.objects.filter(created_by = user.user_profile)
        if posts:
            recent_posts = posts.latest('id')
            post_sub = recent_posts.sub_posted_on
        else:
            recent_posts = None
            post_sub = None
        comments = models.Comment.objects.filter(created_by = user.user_profile)
        if comments:
            recent_comments = comments.latest('id')
            comment_sub = recent_comments.parent_post.sub_posted_on
        else:
            recent_comments = None
            comment_sub = None
    else:
        subs = models.Sub.objects.all()
        messages.add_message(request,messages.ERROR,'Redirected to home. You need to login first')
        return render(request,'allSubs.html',{'subs' : subs})
        #recent_posts,recent_comments = None,None
    return render(request, 'home.html', {'user': request.user, 'post': recent_posts, 'comment' : recent_comments,'comment_sub' : comment_sub, 'comment_post' : post_sub})

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
                messages.add_message(request,messages.SUCCESS,'Successful login')
            else:
                messages.add_message(request,messages.ERROR,'No such user exists.Try again')
                #print('No such user exists.Try again')
            return HttpResponseRedirect(reverse('home'))
        else:
            print('Something went wrong')
            return HttpResponseRedirect(reverse('home'))

def logout_view(request):
    #Logout the current user i.e. flush user related session data
    if request.user.is_authenticated:
        logout(request)
        print(f'User now is {request.user}')
        messages.add_message(request,messages.INFO,'You have logged out.')
        return HttpResponseRedirect(reverse('all-subs'))
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
            messages.add_message(request,messages.SUCCESS,'Account created')
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('signup')) 


def create_sub_view(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = forms.SubForm()
            return render(request,'createSub.html',{'form' : form})
        elif request.method == 'POST':
            submitted_form = forms.SubForm(request.POST)
            if submitted_form.is_valid():
                new_sub = submitted_form.save(commit = False) #Hold off on saving this to the database
                new_sub.created_by = request.user.user_profile
                new_sub.save()
                #No need to use the save_m2m as no many to many relationship data comes from the form
                print('Succesfully created new sub!')
                messages.add_message(request,messages.SUCCESS,f'Created {new_sub.name}')
                return HttpResponseRedirect(reverse('get-posts', kwargs = {'sub_id' : new_sub.id}))
    else:
        return HttpResponseRedirect(reverse('home'))

def create_post_view(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            #Render form
            form = forms.PostForm()
            return render(request,'createPost.html',{'form': form})
        elif request.method == 'POST':
            submitted_form = forms.PostForm(request.POST)
            if submitted_form.is_valid():
                new_post = submitted_form.save(commit = False) #Hold off on saving this to the database
                new_post.created_by = request.user.user_profile
                new_post.save()
                #No need to use the save_m2m as no many to many relationship data comes from the form
                print('Succesfully created new post!')
                return HttpResponseRedirect(reverse('home'))

    else:
        return HttpResponseRedirect(reverse('home'))        

def profile_view(request):
    if request.user.is_authenticated:
        user = request.user.user_profile
        subs = user.created_subs
        posts = user.posts_created
        comments = user.comments_made
        return render(request,'profile.html',{'subs':subs,'comments' : comments, 'posts':posts})
    else:

        return HttpResponse('You need to log in first')

def profile_dashboard_view(request):
    if request.user.is_authenticated:
        user = request.user
        #return HttpResponse('Yet to implement')
        #subscriptions = Implement subscriptions model
        return render(request,'dashboard.html',{'user':user})
    else:
        #Add flash message here
        messages.add_message(request,messages.INFO,'You need to be logged in.')
        return HttpResponseRedirect(reverse('home'))

def sub_dashboard_view(request,sub_id):
    print(f'Requested id is {sub_id}')
    name = models.Sub.objects.get(pk = sub_id).name
    return render(request,'subDashboard.html', {'id' : sub_id, 'name' : name})

def sub_dashboard_data(request, sub_id):
    print('Got an AJAX request')
    sub = models.Sub.objects.get(pk = sub_id)
    sub_posts =  sub.posts
    sub_comments = models.Comment.objects.filter(parent_post__sub_posted_on__id = sub_id)
    members = sub.members.count()
    post_contributors = sub_posts.values('created_by').order_by().annotate(Count('created_by')).count()
    comment_contributors = sub_comments.values('created_by').order_by().annotate(Count('created_by')).count()
    data = {'posts' : sub_posts.count(), 'members'  : members, 'comments' : sub_comments.count(), 'Posters' : post_contributors, 'Commenters' : comment_contributors}
    return JsonResponse({'data' : data})

def create_comment_view(request):
        if request.user.is_authenticated:
            if request.method == 'GET':
                #Render form
                form = forms.CommentForm()
                return render(request,'createComment.html',{'form': form})
            elif request.method == 'POST':
                submitted_form = forms.CommentForm(request.POST)
                if submitted_form.is_valid():
                    new_comment = submitted_form.save(commit = False) #Hold off on saving this to the database
                    new_comment.created_by = request.user.user_profile
                    new_comment.save()
                    post = new_comment.parent_post
                    #No need to use the save_m2m as no many to many relationship data comes from the form
                    print('Succesfully created new comment!')
                    return HttpResponseRedirect(reverse('get-comments',kwargs = {'post_id' : post.id}))

        else:
            return HttpResponseRedirect(reverse('home'))

def get_chart_view(request):
    user = request.user
    #subscriptions = Implement subscriptions model
    posts = user.user_profile.posts_created.count()
    comments = user.user_profile.comments_made.count()
    subs = user.user_profile.created_subs.count()
    data = {'posts' : posts, 'comments' : comments, 'subs' : subs}
    #return JsonResponse({'posts' : posts, 'comments' :comments,'subs' : subs})
    return JsonResponse({'data' : data})

def all_subs_view(request):
    user = request.user
    subs = models.Sub.objects.all()
    return render(request,'allSubs.html',{'subs':subs,'user':user})

def rising_subs_view(request):
    subs = models.Sub.objects.all()
    return render(request,'allSubs.html',{'subs' : subs})

def get_posts_for_sub(request,sub_id):
    sub = models.Sub.objects.get(pk = sub_id)
    posts = models.Post.objects.filter(sub_posted_on__pk = sub_id)
    return render(request,'posts.html',{'sub' : sub, 'posts' : posts,'id' : sub_id})

def get_comments_for_post(request,post_id):
    post = models.Post.objects.get(pk = post_id)
    sub = post.sub_posted_on
    comments = post.comments.all()
    comments = models.Comment.objects.filter(parent_post__id = post_id)
    analyzer = SentimentIntensityAnalyzer()
    #Getting overall polarity
    positive,negative = 0,0
    for comment in comments:
        scores = list(analyzer.polarity_scores(comment.content).values())
        positive += scores[2]
        negative += scores[0]
    if positive > negative:
        sentiment = 'Positive'
    elif positive < negative:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return render(request,'comments.html',{'sub' : sub, 'post': post, 'comments' : comments,'sentiment' : sentiment})

def random_view(request, num = None):
    print(request.GET)
    print(num)
    messages.add_message(request,messages.INFO,'Hi!')
    
    return render(request,'random.html')

'''
def get_post_sentiment(request,post_id):
    comments_ = models.Comment.objects.filter(parent_post__id = post_id)
    text = ''
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    #print(scores)
    for comment in comments_:
        text += ' ' + comment.content 
    #print(text)
    #print(scores.values())
    list_scores = list(scores.values())
    #print(type(list_scores))
    sentiment = None
    if list_scores[2] > list_scores[1]:
        sentiment = 'Positive'
    elif list_scores[2] < list_scores[1]:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    #print(list_scores)
    print('Overall sentiment of the post is:')
    return HttpResponse('Hi')
'''