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
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            #return redirect('home')
    else:
        form = UserCreationForm()
        
    return render(request, 'signup.html', {'form':form})