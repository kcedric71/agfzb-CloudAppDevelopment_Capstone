import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    response = requests.Response()
    try:
        # Call get method of requests library with URL and parameters
        #if "api_key" in kwargs.keys():
       #     print("ok")
        #    api_key = kwargs["api_key"]
        #    params = dict()
        #    params["text"] = kwargs["text"]
            #params["version"] = kwargs["version"]
        #    params["features"] = kwargs["features"]
        #    params["return_analyzed_text"] = kwargs["return_analyzed_text"]
        #    response = requests.get(url, headers={'Content-Type': 'application/json'},
         #                           params=params, auth=HTTPBasicAuth('apikey', api_key))
        #else:
        #    print("nok")
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print(kwargs)
    response = requests.post(url, json=json_payload, params=kwargs)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result 
        #["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id(url, **kwargs):
    print(kwargs)
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        dealer = json_result[0]
        print(dealer)
        #dealer_doc = dealers["body"]
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"])
        results.append(dealer_obj)
    return results 

def get_dealers_by_state(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result 
        #["body"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["data"]["docs"]
        #["body"]
        # For each dealer object
        for review in reviews:
            review_obj = DealerReview(id=review["id"],name=review["name"],dealership=review["dealership"],
                        review=review["review"],purchase=review["purchase"],purchase_date=review["purchase_date"],
                        car_make=review["car_make"],car_model=review["car_model"],car_year=review["car_year"],
                        sentiment="")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text_to_analyze):
    watson_url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/1ddb3e6f-249a-412e-8fd9-5dd2cde31d26"
    watson_api_key = "jtOREZnQJwVRPQWtxtIk5kmHz3TxeuJ5BwYYLtA3ASXD"
    
    authenticator = IAMAuthenticator(watson_api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 
    natural_language_understanding.set_service_url(watson_url) 
    response = natural_language_understanding.analyze( text=text_to_analyze ,features=Features(sentiment=SentimentOptions(targets=[text_to_analyze]))).get_result() 
    label=json.dumps(response, indent=2) 
    label = response['sentiment']['document']['label'] 
    return(label) 


