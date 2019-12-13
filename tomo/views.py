from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
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
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            #login(request, user)
            return redirect('templates\login.html')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form':form})


# Detail of the Event
def detail(request, event_id):
    try:
        event = Event.object.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    
    context = {
        'event': event
    }
    return render(request, 'templates/detail.html', context)