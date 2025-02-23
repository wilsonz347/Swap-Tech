from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .forms import *
from .models import *

#sustainability/views.py - maintains all logic to handle backend-frontend interaction

#home landing page - to be adjusted later
def landing(request):
    return render(request, 'realsite.html')


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
                if user.accountType == "RECYCLE":
                    return redirect('/recyclerhome/')
                else:
                    return redirect('/home/')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def recycler_home(request):
    user = request.user  # Get the logged-in user
    profile = UserProfile.objects.filter(user=user).first()  # Fetch the user's profile if it exists
    listings = Device.objects.filter(listing_user=user)  # Fetch the user's device listings

    context = {
        #'firstname': user.first_name,
        #'lastname': user.last_name,
        #'username': username,  #get user
        'profile': profile,
        'profile_image': profile.profile_image.url if profile and profile.profile_image else None,  #profile image URL
        'notifications': profile.notifications if profile else 0,  #notification count
        'listings': listings,  #listings
    }
    
    return render(request, 'recyclerhome.html', context)


def refurbisher_home(request):
    return render(request, 'refurbhome.html')

def chatbot(request):
    return render(request, 'chatbot.html')


def logout_page(request):
    if request.method == "POST":
        logout(request)
        return redirect('/login/')
    return render(request, 'logout.html')

def register_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            account_type = form.cleaned_data.get('account_type')
            
            # Automatically log in the user after registration
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.info(request, "Account created and logged in successfully!")
                if user.accountType == "RECYCLE":
                    return redirect('recyclerhome')
                else:
                    return redirect('home')
        else:
            messages.error(request, "Error creating account. Please try again.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def marketplace(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
    
    devices = Device.objects.all()
    filters = {
        'sort_options': ['Price', 'Name', 'Date'],
        'current_sort': request.GET.get('sort', 'Price')
    }
    context = {
        'page_title': 'Marketplace',
        'user_profile': user_profile,
        'devices': devices,
        'filters': filters
    }
    return render(request, 'purchase.html', context)


######################################################################