from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.

def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User exists') 
            else:
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email)
                user.save()
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)         
        else:
            pass_err = 'Password are not the same'
            return render(request, 'register.html', {"pass_err": pass_err})
        return redirect('/')
    else:
        return render(request, 'register.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user != None:
            auth.login(request, user)
            return redirect('/')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
