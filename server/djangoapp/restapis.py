# This file contains the code to call the REST APIs
from .models import CarDealer, DealerReview
# Environment variables
from decouple import config
import logging
# IBM Cloudant SDK
from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1, Document
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

DB_NAME = config('CLOUDANT_DB_NAME')

cloudant_authenticator = IAMAuthenticator(config('CLOUDANT_API_KEY'))
watson_authenticator = IAMAuthenticator(config('WATSON_API_KEY'))

cloudant_client = CloudantV1(authenticator=cloudant_authenticator)
cloudant_client.set_service_url(config('CLOUDANT_SERVICE_URL'))

# Natural Language Understanding
nlp = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=watson_authenticator
)
nlp.set_service_url(config('WATSON_SERVICE_URL'))

logger = logging.getLogger(__name__)


def get_sentiment(text):
    try:
        response = nlp.analyze(
            text=text,
            features=Features(sentiment=SentimentOptions())).get_result()
        if response:
            res = response['sentiment']['document']['label']
            return res
    except ApiException as ae:
        logger.error("Method failed with status code " +
                     str(ae.code) + ": " + ae.message)


def get_document_data(doc_id='reviews', **kwargs):
    results = []
    try:
        document = cloudant_client.get_document(
            db=DB_NAME,
            doc_id=doc_id,
        ).get_result()
        if not kwargs:
            return document['data']
        else:
            for ent in document['data']:
                for att, value in kwargs.items():
                    if ent[att] == value:
                        results.append(ent)
            return results
    except ApiException as ae:
        if ae.code == 404:
            print(f'Document with id "{doc_id}" not found in "{DB_NAME}" '
                  'database.')
        else:
            print(ae)


def add_review_to_cloudant(new_obj):
    try:
        curr_doc = cloudant_client.get_document(
            db=DB_NAME,
            doc_id='reviews',
        ).get_result()
        new_doc = curr_doc.copy()
        curr_doc['data'].append(new_obj)
        new_doc['data'] = curr_doc['data']
        cloudant_client.post_document(
            db=DB_NAME,
            document=new_doc
        ).get_result()

    except ApiException as ae:
        if ae.code == 404:
            print('Cannot delete document because either ' + ae)


test_doc = {
    "name": "Nina",
}


def get_dealers_from_cloudant(**kwargs):
    # Get the data from Cloudant
    data = get_document_data(doc_id='dealerships', **kwargs)
    if data:
        dealers = []
        for dealer in data:
            # Create a DealerReview object with values in `doc` object
            dealer_obj = CarDealer(
                id=dealer["id"],
                full_name=dealer["full_name"],
                city=dealer["city"],
                address=dealer["address"],
                zip=dealer["zip"],
                state=dealer["st"],
            )
            dealers.append(dealer_obj)
    return dealers


def get_dealer_reviews_from_cloudant(**kwargs):
    # Get the data from Cloudant
    data = get_document_data(doc_id='reviews', **kwargs)
    if data and len(data) > 0:
        reviews = []
        for review in data:
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                purchase_date=review["purchase_date"],
                review=review["review"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment=get_sentiment(review["review"]),
                id=review["id"]
            )
            reviews.append(review_obj)
        return reviews
    else:
        return []
