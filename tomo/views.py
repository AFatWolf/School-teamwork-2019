from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.utils import timezone
from django.http import Http404, JsonResponse
from .models import Attend, Host, Tag, Event, Comment, User, SignUpForm
from .helper import *
from .forms import *
import datetime
import pytz
from django.contrib import messages
import random


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
                'wrongUsername': True,
                'notLogin': True,
            }
            return render(request, 'login.html', context)
        if authenticate(username=username, password=password) == None:
            context = {
                'wrongPassword': True,
                'notLogin': True,
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
            context = {
                'notLogin': True
            }
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

        tags = current_user.tags.all()
        dict_tag = {}
        i=0
        for t in tags:
            if len(getEventWithTags(tags[i:i+1]))!=0:
                ewt = getEventWithTags(tags[i:i+1])
                dict_tag[t.name]=ewt
            i+=1

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
        # if user picked a date
        if 'date' in request.GET:
            print("Date is in request GET")
            print("Data is: {}".format(request.GET["date"]))
            pivot = datetime.datetime.strptime(request.GET["date"], "%m/%d/%Y")
            pivot = pytz.UTC.localize(pivot)
            list_date_data.append(pivot)
            sorted_list_date = sorted(list_date_data)
            sorted_list_date = sorted_list_date[sorted_list_date.index(pivot):]
            print("List date: ", list_date_data)
            print("Sorted list date: ", sorted_list_date);
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
            data = { 
                'events': events,
                'user': current_user,
                'state':0, # display the calendar display
                'date_list': dict_date,
            }
            print(dict_date)
            return render(request, 'index_calendar.html',data)

        # if date not in GET
        data = { 
            'events': events,
            'user': current_user,
            'state': state,
            'date_list': dict_date,
            'dict_tag': dict_tag,
        }
        return render(request, 'index.html', data)

    else:
        tags=Tag.objects.all()
        dict_tag = {}
        for c in range(0,5):
            i = random.randint(0,len(tags)-1)
            t=tags[i]
            dict_tag[t.name]=getEventWithTags(tags[i:i+1])
        events = Event.objects.all()

        data = { 
            'events': events,
            'dict_tag': dict_tag,
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
        event.name = request.POST.get('name', event.name)
        event.detail= request.POST.get('detail', event.detail)
        # event.hosted_at = request.POST['hosted_at']
        # set adress
        address = request.POST.get('address', event.address)
        print("Address: ", address)
        print("Event address: ", event.address)
        # check if the address change
        if event.address != address:
            location = findGeocoding(address)
            if location and location['lat'] != -1 and location['lng'] != -1:
                event.address = address
                event.lat = location['lat']
                event.lng = location['lng']
        tags_id = request.POST.getlist('tags')
        all_tags = Tag.objects.all()
        # reset tags
        for tag in all_tags:
            event.tags.remove(tag)
        # add the new tags
        for tag_id in tags_id:
            tag = Tag.objects.get(pk=tag_id)
            event.tags.add(tag)

        # handle images
        form = UploadEventImageForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()

        event.save()
        return redirect(detail, event_id)

    # GET
    tags = Tag.objects.all()
    event_tags = event.tags.all()
    print(event_tags)
    try:
        user_id = getCurrentUserId(request)
        user = User.objects.get(pk=user_id)
        form = UploadEventImageForm()

        context = {
            'event': event,
            'tags': tags,
            'event_tags' : event_tags,
            'user': user,
            'form': form,
        }
    except:
        context = {
            'event': event,
            'tags': tags,
            'event_tags': event_tags,
        }
    print("Context for update: ", context)
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
    if request.method=="POST" :
        edit.first_name = request.POST.get('first_name')
        edit.last_name = request.POST.get('last_name')
        edit.description = request.POST.get('description')
        edit.age = request.POST.get('age')  
        edit.email = request.POST.get('email')
        edit.save()
    form = {
            'edit' : edit
    }
  
    return render(request, 'settings.html', form)


def password_update(request):
    edit = User.objects.get(pk=getCurrentUserId(request))
    if request.method=="POST":
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
            'form':form
    }
    return render(request, 'password.html', change) 
    
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

def search(request):
    if request.method == 'GET':
        query = request.GET.get('q', 'a' * 10).lower() 
        events = Event.objects.all()
        users = User.objects.all()
        results = []
        for event in events:
            if query in event.name.lower():
                results.append(event)
        for user in users:
            if query in user.username.lower()  or query in user.first_name.lower() or query in user.last_name.lower():
                    results.append(user)
        print("Query: ", query)
        print("Return: ", results)
        context = {
            'results': results,
        }
        return render(request, "search_results.html", context)


