from .models import CarModel, CarMake, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, post_request
from django.shortcuts import render, redirect
from django.urls import reverse
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf
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


def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/get-dealers"
        dealer = get_dealer_by_id_from_cf(dealer_url, id)
        context["dealer"] = dealer
        context["dealer_id"] = id
        print("LINE102:", dealer)

        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/reviews"
        reviews = get_dealer_reviews_from_cf(review_url, id)
        # print("Reviews from line 113", reviews)
        context["reviews"] = reviews

        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review


"""
def add_review(request, id):
    context = {}
    if request.method == "GET":
        logger.debug('GET:')
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/reviews"
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/get-dealers"
        dealer = get_dealer_by_id_from_cf(url, id)

        # Assuming you have a 'dealer_id' field in the CarModel model
        cars = CarModel.objects.all()

        context["cars"] = cars
        context["dealer"] = dealer
        print("result 128:", cars, dealer)
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        logger.debug('POST:')
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/post-review"
        print("REQUEST:", request.POST)
        if 'purchasecheck' in request.POST:
            was_purchased = True
        else:
            was_purchased = False
        cars = CarModel.objects.filter(id=id)
        for car in cars:
            if car.id == int(request.POST['car']):
                review_car = car
        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["name"] = request.POST['full_name']
        review["dealership"] = id
        review["review"] = request.POST['content']
        review["purchase"] = was_purchased
        review["purchase_date"] = request.POST['purchasedate']
        review["car_make"] = review_car.make.name
        review["car_model"] = review_car.name
        review["car_year"] = review_car.year.strftime("%Y")
        json_payload = {}
        json_payload["review"] = review
        response = post_request(url, json_payload)
        return redirect("djangoapp:dealer_details", id=id)



def add_review(request, id):
    if request.user.is_authenticated:
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/get-dealers"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
        if request.method == "GET":
            cars = CarModel.objects.all()
            context["cars"] = cars
            print(context)
            return render(request, 'djangoapp/add_review.html', context)

        if request.method == "POST":
            review = {}
            review["name"] = request.user.first_name + \
                " " + request.user.last_name
            form = request.POST
            review["dealership"] = id
            review["review"] = form["content"]
            if (form.get("purchasecheck") == "on"):
                review["purchase"] = True
            else:
                review["purchase"] = False
            if (review["purchase"]):
                review["purchase_date"] = form["purchasedate"]
                car = CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year
            post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/post-review"
            json_payload = {"review": review}
            post_request(post_url, json_payload, id=id)
            return redirect("djangoapp:dealer_details", id=id)
    else:
        return redirect("/djangoapp/login")
"""


def add_review(request, id):
    context = {}
    dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/get-dealers"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars

        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            logger.debug('DEBUG:')
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/3cd318ff-d3b8-46d8-b5de-e37b3f6b0123/api/post-review"
            post_request(review_post_url, new_payload, id=id)
        return redirect("djangoapp:dealer_details", id=id)
