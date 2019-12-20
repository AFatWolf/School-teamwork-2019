from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.http import Http404
from .models import Attend, Host, Tag, Event, Comment, User, SignUpForm
from .helper import *

# def user(request):
#     if 

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username=username, password=password)
            #login(request)
            #login(signup)
            return redirect('login')
    else:
        form = SignUpForm()
        
    return render(request, 'signup.html', {'form':form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            context = {
                'wrongUsername': True 
            }
            return render(request, 'login.html', context)
        if authenticate(username=username, password=password) == None:
            context = {
                'wrongPassword': True
            }
            return render(request, 'login.html', context)
        else:
            try:
                setUserId(request, username=username)
            except Exception as e:
                print(e)
            if user.first_time:
                user.first_time = 0
                return redirect(addTags)
            else:
                return redirect(index)
    else:
        if getCurrentUserId(request) != NO_USER:
            return redirect(index)
        else:
            context = {}
            return render(request, 'login.html', context)

def logout(request):
    deleteCookieUserId(request)
    return redirect(login)

def addTags(request):
    user_id = getCurrentUserId(request)
    user = User.objects.get(id=user_id)
    # if not first time log in
    if int(user.first_time) == 0:
        print(user.first_time)
        return redirect(index)
    else:
        if request.method == 'GET':
            tags = Tag.objects.all()
            context = {
                'tags': tags,
            }
            return render(request, 'addtags.html', context)
        elif request.method == 'POST':
            tags_id = request.POST.getlist('tags')
            print("Tags from checkbox: ", tags_id)
            for tag_id in tags_id:
                tag = Tag.objects.get(pk=tag_id)
                user.tags.add(tag)
            print("User tags: ", user.tags.all())
            return redirect(index)


def index(request):
    if getCurrentUserId(request) != NO_USER:
        current_user = User.objects.get(pk=getCurrentUserId(request))
        print("Hey ", getCurrentUserId(request))
        events = Event.objects.all()
        data = { 
            'events': events,
            'user': current_user,
        }
    else:
        print("No no")
        print("Hey ", getCurrentUserId(request))
        events = Event.objects.all()
        data = { 'events': events,
        }
    print(data)
    return render(request, 'index.html', data)

# Detail of the Event
def detail(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    if request.method == 'POST':
        try:
            comment = Comment(event=event, text=request.POST['comment_text'], date=timezone.now())
            comment.save()
        except:
            pass
    
    context = {
        'event': event,
        'comment': event.comments.order_by('-posted_at')
    }
    return render(request, 'detail.html', context)

def update(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.method == 'POST':
        event.name = request.POST['name']
        event.detail= request.POST['detail']
        event.hosted_at = request.POST['hosted_at']
        event.save()
        return redirect(detail, event_id)

    context = {
        'event': event,
    }
    return render(request, 'update.html', context)

def create(request):
    if request.method == 'POST':
        event = Event.objects.create(
            name = request.POST['title'],
            detail = request.POST['detail'],
            hosted_at = request.POST['hosted_at']
        )
        return redirect('detail', event.id)
    return render(request, 'create.html')


def settings(request):
    edit = User.objects.get(pk=getCurrentUserId(request))
    if request.method == 'POST':
        edit.first_name = request.POST.get('first_name')
        edit.last_name = request.POST.get('last_name')
        edit.description = request.POST.get('description')
        edit.age = request.POST.get('age')
        edit.new_password = request.POST.get('new_password')
        edit.confirm_password = request.POST.get('confirm_passowrd')  # reconfirm password

        
        if authenticate(username=edit.username, password=request.POST['password']) == None and edit.confirm_password == edit.new_password:
            edit.password = edit.new_password
            edit.password.save()
            return redirect("login")  
        
    return render(request, 'settings.html')

    
def profile(request, user_name):
    try:
        user = User.objects.get(username=user_name)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)
