from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {
        'title': 'Contact',
        'email': 'shaar.nate@gmail.com'
    }
    return render(request, 'djangoapp/contact.html', context)


def login_request(request):
    if request.method == "POST":
        # Get the username and password provided by the user
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(username=username, password=password)
        # if the user is authenticated
        if user is not None:
            # Longin the user
            login(request, user)
            # Display a success message
            messages.success(request, "You have successfully logged in")
            # Redirect to the index page (homepage)
            return redirect('djangoapp:index')

        else:
            # User is not authenticated
            messages.error(request, "Invalid username or password.")
    return render(request, 'djangoapp/indexhtml')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('djangoapp:registration')
        else:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password, email=email)
            user.save()
            login(request, user)
            messages.info(request, "You have successfully registered")
            return redirect('djangoapp:index')
    return render(request, 'djangoapp/registration.html')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {
        'title': 'Home'
    }
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
