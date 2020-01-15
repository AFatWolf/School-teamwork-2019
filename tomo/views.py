from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.utils import timezone
from django.http import Http404, JsonResponse
from .models import Attend, Host, Tag, Event, Comment, User, SignUpForm
from .helper import *
import datetime
import pytz
from django.contrib import messages


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
            first_name= form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email= form.cleaned_data.get('email')
            user = User.objects.create_user(username=username, password=password, first_name = first_name, last_name=last_name, email=email)
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
                'user': user,
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
        date_data = Event.objects.values_list('hosted_at', flat=True).order_by('-hosted_at')
        list_date_data = list(date_data)
        sorted_list_date = sorted(list_date_data, reverse=True)

        date_list=[]
        for d in sorted_list_date:
            date = d.strftime("%A, %B %#d, %Y")
            if date not in date_list:
                date_list.append(date)
        dict_date = {}
        for d in date_list:
            new_list=[]
            for e in events:
                if e.hosted_at.strftime("%A, %B %#d, %Y") == d:
                    new_list.append(e)
                    dict_date[d] = new_list
                else:
                    pass

        state=True
        if 'view' in request.GET:
            if request.GET["view"] == "slide":
                state = True
            else:
                events = Event.objects.order_by('-hosted_at')
                state = False
        if 'date' in request.GET:
            pivot = datetime.datetime.strptime(request.GET["date"], "%m/%d/%Y")
            pivot = pytz.UTC.localize(pivot)
            list_date_data.append(pivot)
            sorted_list_date = sorted(list_date_data, reverse=True)
            sorted_list_date = sorted_list_date[:sorted_list_date.index(pivot)+1]
            date_list=[]
            for d in sorted_list_date:
                date = d.strftime("%A, %B %#d, %Y")
                if date not in date_list:
                    date_list.append(date)
            dict_date = {}
            for d in date_list:
                new_list=[]
                for e in events:
                    if e.hosted_at.strftime("%A, %B %#d, %Y") == d:
                        new_list.append(e)
                        dict_date[d] = new_list
                    else:
                        pass
            print("sorted: ",sorted_list_date)
            data = { 
                'events': events,
                'user': current_user,
                'state': state,
                'date_list': dict_date,
            }
            return render(request, 'index.html',data)
            # return redirect(index)
            print("Render:")
            print(render(request, 'index.html',data).content)
            return render(request, 'index.html',data)
            # return redirect(index)
        data = { 
            'events': events,
            'user': current_user,
            'state': state,
            'date_list': dict_date,
        }
        print("sorted out side: ",sorted_list_date)
    else:
        print("No no")
        print("Hey ", getCurrentUserId(request))
        events = Event.objects.all()
        data = { 'events': events,
        }
    return render(request, 'index.html', data)

# Detail of the Event
def detail(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    if request.method == 'POST':
        try:
            Comment.objects.create(event=event, content=request.POST['comment_text'], date=timezone.now())
        except:
            pass
    context = {
        'event': event,
        'comments': event.comments.order_by('-date')
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
        #if authenticate(username=edit.username, password=request.POST['password']) == None:

        form = PasswordChangeForm(edit.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('logout') 

        else:
             messages.error(request, 'Please correct the error below.')
             return redirect('settings')   
    else:
            form = PasswordChangeForm(request.user)
                
    change = {
            'edit':edit,
            'form':form
    }
    return render(request, 'settings.html', change) 
    
    #return render(request, 'settings.html' )

'''
def change_password(request):
    user = User.objects.get(pk=getCurrentUserId(request))
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            #user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'settings.html', {
        'form': form
    }) '''
    
def profile(request, user_name):
    try:
        user = User.objects.get(username=user_name)
    except Event.DoesNotExist:
        raise Http404("User does not exist")
    
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)
