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

# Create an `about` view to render a static about page
def about(request):
    return render(request, "djangoapp/about.html")


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, "djangoapp/contact.html")

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    defaultUrl = 'djangoapp/index.html'
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['userpassword']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, defaultUrl, context)
    else:
        return render(request, defaultUrl, context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    username = request.POST['username']
    password = request.POST['userpassword']
    firstname = request.POST['userfirstname']
    lastname = request.POST['userlastname']
    isUserAvailable = False

    try:
        User.objects.get(username=username)
        isUserAvailable = True
    except:
        isUserAvailable = False

    if isUserAvailable:
        return render(request, 'djangoapp/registration.html', {})
    else:
        user = User.objects.create_user(
            username=username, first_name=firstname, last_name=lastname, password=password)
        login(request, user)
        return redirect("djangoapp:index")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealerId):
    context = {}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/8ce6fac2-d8dd-421f-b11e-f066c1336a48/dealership-package/get-dealership"
        urlReviews = "https://eu-gb.functions.appdomain.cloud/api/v1/web/8ce6fac2-d8dd-421f-b11e-f066c1336a48/dealership-package/get-review"
        context["dealerInfo"] = get_dealer_by_id(url, dealerId)
        context["dealerReviews"] = get_dealer_reviews_from_cf(
            urlReviews, dealerId)
        context["dealerId"] = dealerId

        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealerId):
    # User must be logged in before posting a review
    if request.user.is_authenticated:
        if request.method == "GET":
            context = {
                "cars": CarModel.objects.all(),
                "dealerId": dealerId,
            }
            return render(request, 'djangoapp/add_review.html', {"context": context})
        if request.method == "POST":
            form = request.POST
            review = dict()
            review["review_id"] = random.randint(1000, 9999)
            review["name"] = request.user.first_name + \
                " " + request.user.last_name
            review["dealership"] = dealerId
            review["review"] = form["reviewtext"]
            if "iscarpurchased" in form:
                review["purchase"] = True
                review["purchase_date"] = datetime.strptime(
                    form.get("purchasedate"), "%m/%d/%Y").isoformat()
            else:
                review["purchase"] = False
                review["purchase_date"] = None
            car = CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.model_make.make_name
            review["car_model"] = car.model_name
            review["car_year"] = car.model_year

            # API Cloud Function route
            url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/8ce6fac2-d8dd-421f-b11e-f066c1336a48/dealership-package/post-review"
            # Create a JSON payload that contains the review data
            json_payload = {"review": review}
            # Performing a POST request with the review
            result = post_request(url, json_payload, dealerId=dealerId)
            if int(result.status_code) == 200:
                print("Review posted successfully.")

            # After posting the review the user is redirected back to the dealer details page
            return redirect("djangoapp:dealer_details", dealerId)
    else:
        return redirect("/djangoapp/login")
