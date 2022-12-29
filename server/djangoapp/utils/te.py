import json
import logging
from decouple import config
from ibm_cloud_sdk_core import ApiException
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Set logging level to show only critical logs
logging.basicConfig(level=logging.CRITICAL)

cloudant_authenticator = IAMAuthenticator(config('CLOUDANT_API_KEY'))

client = CloudantV1(authenticator=cloudant_authenticator)
client.set_service_url(config('CLOUDANT_SERVICE_URL'))

# 2. Update the document ==============================================
example_db_name = config('CLOUDANT_DB_NAME')
example_doc_id = "reviews"

with open('revs.json', 'r') as file:
    # Load JSON data
    rees = json.load(file)

# Add an entry to the rees list
# rees.append({

# Try to get the document if it previously existed in the database
try:
    document = client.get_document(
        db=example_db_name,
        doc_id=example_doc_id
    ).get_result()

    new_doc = document.copy()
    document['data'].append({
        "name": "Roula",
    })

    new_doc['data'] = document['data']

    #  Remove the joined property from document object
    # if "joined" in document:
    #     document.pop("joined")

    # Update the document in the database
    update_document_response = client.post_document(
        db=example_db_name,
        document=new_doc
    ).get_result()

    # =================================================================
    # Note 2: updating the document can also be done with the
    # "put_document" function. `doc_id` and `rev` are required for an
    # UPDATE operation, but `rev` can be provided in the document
    # object as `_rev` too:
    """
    update_document_response = client.put_document(
        db=example_db_name,
        doc_id=example_doc_id,  # doc_id is a required parameter
        rev=document["_rev"],
        document=document  # _rev in the document object CAN replace above `rev` parameter
    ).get_result()
    """
    # =================================================================

    # Keeping track of the latest revision number of the document
    # object is necessary for further UPDATE/DELETE operations:
    document["_rev"] = update_document_response["rev"]
    print(f'You have updated the document:')

except ApiException as ae:
    if ae.code == 404:
        print('Cannot delete document because either ' +
              f'"{example_db_name}" database or "{example_doc_id}" ' +
              'document was not found.')
