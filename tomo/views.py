from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.http import Http404
from .models import Attend, Host, Tag, Event, Comment


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = AuthUser.objects.get(username=username)
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
            context = {}
            print("OK")
            return index(request)
    else:
        context = {}
        return render(request, 'login.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            #login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form':form})

def index(request):
    events = Event.objects.all()
    data = { 'events': events }
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
