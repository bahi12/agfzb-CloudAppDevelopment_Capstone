from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_from_cf_by_id, post_request
from django.shortcuts import render, redirect
from django.urls import reverse
from .restapis import get_dealers_from_cf, get_dealer_from_cf_by_id
import json
import logging
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import sys
sys.path.append('.')
# from .models import related models
# from .restapis import related methods
# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
# def contact(request):
def contact(request):
    return render(request, 'djangoapp/contact_us.html')
# Create a `login_request` view to handle sign in request
# def login_request(request):


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password!"
            return render(request, 'djangapp/registration.html')
# Create a `logout_request` view to handle sign out request
# def logout_request(request):


def logout_request(request):
    logout(request)
    return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
# def registration_request(request):


def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error('New user')
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = 'User alreay exists!'
            return render(request, 'djangoapp/registration.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships


def get_dealerships(request):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/get-dealership"
    dealerships = get_dealers_from_cf(url)
    context = {'dealership_list': dealerships}

    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://e29b86ca.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_from_cf_by_id(dealer_url, id=dealer_id)
        context["dealer"] = dealer
    
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/get-dealers"
        reviews = get_dealer_reviews_from_cf(review_url, id=dealer_id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review


def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://e29b86ca.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_from_cf_by_id(url, dealer_id)
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context["cars"] = cars
        context["dealer"] = dealer
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        url = "https://e29b86ca.eu-gb.apigw.appdomain.cloud/api/review/"
        if 'purchasecheck' in request.POST:
            was_purchased = True
        else:
            was_purchased = False
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        for car in cars:
            if car.id == int(request.POST['car']):
                review_car = car
        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["name"] = request.POST['name']
        review["dealership"] = dealer_id
        review["review"] = request.POST['content']
        review["purchase"] = was_purchased
        review["purchase_date"] = request.POST['purchasedate']
        review["car_make"] = review_car.make.name
        review["car_model"] = review_car.name
        review["car_year"] = review_car.year.strftime("%Y")
        json_payload = {}
        json_payload["review"] = review
        response = post_request(url, json_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
