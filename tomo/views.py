from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.http import Http404
from .models import *


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            # [0] because it is a query set
            user = User.objects.filter(username=username)[0]
        except:
            context = {
                'wrongUsername': True 
            }
            return render(request, 'login.html', context)
        if password != user.password:
            context = {
                'wrongPassword': True
            }
            return render(request, 'login.html', context)
        else:
            context = {}
            print("OK")
            return render(request, 'login.html', context)
    else:
        context = {}
        return render(request, 'login.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            #return redirect('home')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form':form})


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