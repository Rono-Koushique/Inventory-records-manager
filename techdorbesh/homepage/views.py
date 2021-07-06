from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print('fux')
            login(request, user)
            return redirect('td_database/')
        else:
            messages.info(request, 'Invalid username or password')

    return render(request, 'homepage/home.html', {})

def team(request):
    return render(request, 'homepage/team.html', {})

def logout_user(request):
    logout(request)
    return redirect('home')

def contacts(request):
    return render(request, 'homepage/contacts.html', {})

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created")
            return render(request, 'homepage/home.html', {})

    return render(request, 'homepage/register.html', {'form' : form})