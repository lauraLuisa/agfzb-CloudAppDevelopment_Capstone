from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If it is a new user
            if not user_exist:
                # Create user in auth_user table
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
                # Login the user and redirect to course list page
                login(request, user)
                return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/67df44c4-1b50-476c-87b6-0ec0ea60bc7a/dealership-package/get-dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        # dealer_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/67df44c4-1b50-476c-87b6-0ec0ea60bc7a/dealership-package/get-dealerships"
        # dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        # context["dealer"] = dealer
    
        review_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/67df44c4-1b50-476c-87b6-0ec0ea60bc7a/dealership-package/get-reviews"

        reviews = get_dealer_reviews_from_cf(review_url, id=id)

        context["reviews"] = reviews
        
        # return HttpResponse(reviews)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if user.is_authenticated:
        review = {}
        review["dealership"]: dealer_id
        review["name"]: request.POST['name']
        review["purchase"]: false
        review["review"]: "Great service!"
        review["purchase_date"]: "10/21/2022"
        review["car_make"]: "Toyota"
        review["car_model"]: "Yaris"
        review["car_year"]: "10/21/2022"

        json_payload = {}
        json_payload["review"] = review

        review_post_url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/67df44c4-1b50-476c-87b6-0ec0ea60bc7a/dealership-package/review-post"

        res = post_request(review_post_url, json_payload, dealerId=dealer_id)
        print(res)
        return HttpResponse(res)
