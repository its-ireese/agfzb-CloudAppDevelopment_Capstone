import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core import ApiException
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import SentimentOptions, Features

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred while requesting GET:" + url)
    json_data = json.loads(response.text)
    return json_data

def get_dealer_by_id(url, dealerId):
    results = []
    try:
        json_result = get_request(url, dealerId=dealerId)
        if json_result:
            dealers = json_result["rows"]
            for dealer in dealers:
                dealer_doc = dealer
                dealer_obj = CarDealer()
                if "address" in dealer_doc:
                    dealer_obj.address = dealer_doc["address"]
                if "city" in dealer_doc:
                    dealer_obj.city = dealer_doc["city"]
                if "full_name" in dealer_doc:
                    dealer_obj.full_name = dealer_doc["full_name"]
                if "dealer_id" in dealer_doc:
                    dealer_obj.dealer_id = dealer_doc["dealer_id"]
                if "lat" in dealer_doc:
                    dealer_obj.lat = dealer_doc["lat"]
                if "long" in dealer_doc:
                    dealer_obj.long = dealer_doc["long"]
                if "short_name" in dealer_doc:
                    dealer_obj.short_name = dealer_doc["short_name"]
                if "state" in dealer_doc:
                    dealer_obj.state = dealer_doc["state"]
                if "st" in dealer_doc:
                    dealer_obj.st = dealer_doc["st"]
                if "zip" in dealer_doc:
                    dealer_obj.zip = dealer_doc["zip"]
                results.append(dealer_obj)
    except:
        print("Error")

    return results

def get_dealers_by_state(url, state):
    results = []
    try:
        json_result = get_request(url, state=state)
        if json_result:
            dealers = json_result["rows"]
            for dealer in dealers:
                dealer_doc = dealer["doc"]
                dealer_obj = CarDealer()
                if "address" in dealer_doc:
                    dealer_obj.address = dealer_doc["address"]
                if "city" in dealer_doc:
                    dealer_obj.city = dealer_doc["city"]
                if "full_name" in dealer_doc:
                    dealer_obj.full_name = dealer_doc["full_name"]
                if "dealer_id" in dealer_doc:
                    dealer_obj.dealer_id = dealer_doc["dealer_id"]
                if "lat" in dealer_doc:
                    dealer_obj.lat = dealer_doc["lat"]
                if "long" in dealer_doc:
                    dealer_obj.long = dealer_doc["long"]
                if "short_name" in dealer_doc:
                    dealer_obj.short_name = dealer_doc["short_name"]
                if "state" in dealer_doc:
                    dealer_obj.state = dealer_doc["state"]
                if "st" in dealer_doc:
                    dealer_obj.st = dealer_doc["st"]
                if "zip" in dealer_doc:
                    dealer_obj.zip = dealer_doc["zip"]
                results.append(dealer_obj)
    except:
        print("Error")

    return results

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(f"POST to {url}")
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        print("Network exception occurred while requesting POST:" + url)

    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url):
    results = []
    try:
        json_result = get_request(url)
        if json_result:
            dealers = json_result["rows"]
            for dealer in dealers:
                dealer_doc = dealer["doc"]
                dealer_obj = CarDealer()
                if "address" in dealer_doc:
                    dealer_obj.address = dealer_doc["address"]
                if "city" in dealer_doc:
                    dealer_obj.city = dealer_doc["city"]
                if "full_name" in dealer_doc:
                    dealer_obj.full_name = dealer_doc["full_name"]
                if "dealer_id" in dealer_doc:
                    dealer_obj.dealer_id = dealer_doc["dealer_id"]
                if "lat" in dealer_doc:
                    dealer_obj.lat = dealer_doc["lat"]
                if "long" in dealer_doc:
                    dealer_obj.long = dealer_doc["long"]
                if "short_name" in dealer_doc:
                    dealer_obj.short_name = dealer_doc["short_name"]
                if "state" in dealer_doc:
                    dealer_obj.state = dealer_doc["state"]
                if "st" in dealer_doc:
                    dealer_obj.st = dealer_doc["st"]
                if "zip" in dealer_doc:
                    dealer_obj.zip = dealer_doc["zip"]

                results.append(dealer_obj)
    except Exception as inst:
        print("Error", inst)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    try:
        json_result = get_request(url, dealerId=dealerId)
        if json_result:
            reviews = json_result["docs"]
            for review_doc in reviews:
                review_obj = DealerReview()
                if "car_make" in review_doc:
                    review_obj.car_make = review_doc["car_make"]
                if "car_model" in review_doc:
                    review_obj.car_model = review_doc["car_model"]
                if "car_year" in review_doc:
                    review_obj.car_year = review_doc["car_year"]
                if "dealership" in review_doc:
                    review_obj.dealership = review_doc["dealership"]
                if "name" in review_doc:
                    review_obj.name = review_doc["name"]
                if "purchase" in review_doc:
                    review_obj.purchase = review_doc["purchase"]
                if "purchase_date" in review_doc:
                    review_obj.purchase_date = review_doc["purchase_date"]
                if "review" in review_doc:
                    review_obj.review = review_doc["review"]
                    review_obj.sentiment = analyze_review_sentiments(
                        review_doc["review"])
                if "review_id" in review_doc:
                    review_obj.review_id = review_doc["review_id"]
                results.append(review_obj)
    except ApiException as ae:
        errorBody = {"error": ae.message}
        if ("reason" in ae.http_response.json()):
            errorBody["reason"] = ae.http_response.json()["reason"]
    except Exception as inst:
        print(inst)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerReview):
    try:
        authenticator = IAMAuthenticator(
            "4SnfER9xvvOSPjF6bY7puGbPdHvZc1j1uj_lZgOK9GiB")
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2022-11-24',
            authenticator=authenticator
        )

        natural_language_understanding.set_service_url(
            "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/44431eeb-5042-4db2-b8a4-d7f1b8021229")
        response = natural_language_understanding.analyze(
            text=dealerReview, features=Features(sentiment=SentimentOptions())).get_result()
        return response["sentiment"]["document"]["label"]
    except Exception as inst:
        print(inst)
        return "Neutral"


