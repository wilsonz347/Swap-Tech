from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm
from .models import *

#sustainability/views.py - maintains all logic to handle backend-frontend interaction

#home landing page - to be adjusted later
def landing(request):
    return render(request, 'landing.html')


# Authentication methods - login, logout, account registration...

def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            account_type = form.cleaned_data.get('account_type')
            
            # Check if a user with the provided email and account type exists
            if not User.objects.filter(email=email, accountType=account_type).exists():
                messages.error(request, 'Invalid Email or Account Type')
                return redirect('/login/')
            
            # Authenticate the user with the provided email and password
            user = authenticate(email=email, password=password)
            
            if user is None:
                messages.error(request, "Invalid Password")
                return redirect('/login/')
            else:
                login(request, user)
                return redirect('/home/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_page(request):
    if request.method == "POST":
        logout(request)
        return redirect('/login/')
    return render(request, 'logout.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        account_type = request.POST.get('account_type')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, "Username already taken!")
            return redirect('/register/')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            accountType=account_type
        )
        
        # Set the user's password and save the user object
        user.set_password(password)
        user.save()
        
        messages.info(request, "Account created Successfully!")
        return redirect('/login/')
    
    return render(request, 'register.html')


######################################################################