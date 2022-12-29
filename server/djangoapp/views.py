from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cloudant, get_dealer_reviews_from_cloudant, add_review_to_cloudant
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging

# Generate a random hex string for the id (primary key)
from djangoapp.utils.hex_id import generate_hex

# Get an instance of a logger
logger = logging.getLogger(__name__)


def about(request):
    context = {
        'title': 'About',
        'page_header': 'About Us',
    }
    return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {
        'title': 'Contact',
        'page_header': 'Contact Us',
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


def get_dealerships(request):
    context = {
        'title': 'Home',
        'page_header': 'Welcome to Best Dealerships',
        'page_description': 'Are you in the market for a new or used car? Look no further than Best Dealerships! Our site is a go-to resource for finding trustworthy dealership reviews. Use our comprehensive directory to search for dealerships in your area and read reviews from other customers. You can also leave your own review to help others find the best dealership for their needs. Thank you for choosing Best Dealerships for all of your car buying needs!',
    }
    if request.method == "GET":
        # Get dealers from the URL
        dealerships = get_dealers_from_cloudant()
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    context = {
        'title': 'Dealer Details',
        'dealer_id': dealer_id,
    }
    if request.method == "GET":
        # Get the dealer id from the request
        dealer = get_dealers_from_cloudant(id=dealer_id)
        context['page_header'] = dealer[0]
        context['page_description'] = f'{dealer[0].city}, {dealer[0].state}, {dealer[0].zip}'
        reviews = get_dealer_reviews_from_cloudant(dealership=dealer_id)
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    dealer = get_dealers_from_cloudant(id=dealer_id)
    # Get the reviews by this dealer
    reviews = get_dealer_reviews_from_cloudant(dealership=dealer_id)
    # Loop through the review and get the the car make, model and year
    cars = []
    models = []
    years = []
    for review in reviews:
        cars.append(review.car_make)
        models.append(review.car_model)
        years.append(review.car_year)

    context = {
        'title': 'Add Review',
        'page_header': 'Add Review',
        'page_description': dealer[0].full_name,
        'dealer_id': dealer_id,
        'cars': cars,
        'models': models,
        'years': years,
    }

    if request.method == "POST":
        # Construct the new review object
        review = {
            'id': generate_hex(),
            'name': request.user.get_full_name(),
            'dealership': dealer_id,
            'review': request.POST.get('review'),
            'purchase': request.POST.get('purchase-check'),
            'purchase_date': request.POST.get('purchase_date'),
            'car_make': request.POST.get('car_make'),
            'car_model': request.POST.get('car_model'),
            'car_year': request.POST.get('car_year'),
            'review_date': str(datetime.utcnow().date().isoformat()),
        }
        add_review_to_cloudant(review)
        return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
    else:
        return render(request, 'djangoapp/add_review.html', context)
