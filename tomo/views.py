from django.shortcuts import render
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