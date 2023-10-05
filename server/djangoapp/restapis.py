import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import logging

logger = logging.getLogger(__name__)


def get_request(url, **kwargs):
    print(kwargs)
    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={
                                    'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(
                url, headers={'Content-Type': 'application/json'}, params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except Exception as e:
        print("Error ", e)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        print(json_data)
        return json_data
    except:
        print("Network exception occurred")


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            # print('DEALER L54:', dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


"""
def get_dealer_from_cf_by_id(url, id):
    json_result = get_request(url, id=id)

    if json_result:
        if "body" in json_result:
            dealers = json_result["body"]

            dealer_doc = dealers["docs"][0]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                 full_name=dealer_doc["full_name"],
                                 id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                 st=dealer_doc["st"], zip=dealer_doc["zip"])
            return dealer_obj
        else:
            print("The JSON response from the Cloudant database does not contain a key called 'body'")

    return None
"""


def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)
    dealer_obj = None

    if json_result:
        for dealer_data in json_result:
            if 'doc' in dealer_data:
                dealer_doc = dealer_data['doc']
                dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                       id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                       full_name=dealer_doc["full_name"],
                                       st=dealer_doc["st"], zip=dealer_doc["zip"])
                break  # Exit the loop if a valid dealer is found

    return dealer_obj


def get_dealer_reviews_from_cf(url, id):
    results = []
    # Perform a GET request with the specified dealer id
    # print("RESULTS BEFORE", results)
    json_result = get_request(url, id=id)
    # print("JSON Result:", json_result)  # Add this line for debugging
    if json_result:
        # Get all review data from the response

        reviews = json_result["data"]["docs"]
        # print('L112:', reviews)
        # For every review in the response
        for review in reviews:
            print("Review Data:", review)
            # Create a DealerReview object from the data
            # These values must be present
            review_content = review["review"]
            # Use a different variable name for the review ID
            review_id = review["id"]
            name = review["name"]
            purchase = review["purchase"]
            dealership = review["dealership"]
            try:
                # These values may be missing
                car_make = review["car_make"]
                car_model = review["car_model"]
                car_year = review["car_year"]
                purchase_date = review["purchase_date"]
                # Creating a review object
                review_obj = DealerReview(
                    dealership=dealership, id=review_id, name=name, purchase=purchase, review=review_content,
                    car_make=car_make, car_model=car_model, car_year=car_year, purchase_date=purchase_date)
            except KeyError:
                print("Something is missing from this review. Using default values.")
                # Creating a review object with some default values
                review_obj = DealerReview(
                    dealership=dealership, id=review_id, name=name, purchase=purchase, review=review_content,
                    car_make="N/A", car_model="N/A", car_year="N/A", purchase_date="N/A")

            # Analysing the sentiment of the review object's review text and saving it to the object attribute "sentiment"
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            # print(f"sentiment: {review_obj.sentiment}")

            # Saving the review object to results
            results.append(review_obj)
            # print("RESULTS AFTER", results)

    return results


def analyze_review_sentiments(dealer_review):
    API_KEY = "udjFrCBHWPyMk8TE3-8Q4wRAI7Gf_1Deg2y8g_hCA_2H"
    NLU_URL = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/ebe21a79-1029-47d3-bcba-2fbb9f943b44"
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(NLU_URL)
    response = natural_language_understanding.analyze(text=dealer_review, features=Features(
        sentiment=SentimentOptions(targets=[dealer_review]))).get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return (label)
