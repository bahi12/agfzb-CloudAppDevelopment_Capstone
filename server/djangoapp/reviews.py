from django.http import JsonResponse

from cloudant.client import Cloudant
from cloudant.query import Query
import json



# Add your Cloudant service credentials here
cloudant_username = "COUCH_USERNAME"
cloudant_api_key = "IAM_API_KEY"
cloudant_url = "COUCH_URL"

client = Cloudant.iam(cloudant_username, cloudant_api_key, connect=True, url=cloudant_url)
db = client["reviews"]


def get_reviews(request):
    """Get reviews for a dealership."""

    dealership_id = request.GET.get("id")

    # Check if "id" parameter is missing
    if dealership_id is None:
        return JsonResponse({"error": "Missing 'id' parameter in the URL"}, status=400)

    # Convert the "id" parameter to an integer (assuming "id" should be an integer)
    try:
        dealership_id = int(dealership_id)
    except ValueError:
        return JsonResponse({"error": "'id' parameter must be an integer"}, status=400)

    # Define the query based on the 'dealership' ID
    selector = {
        "dealership": dealership_id
    }

    # Execute the query using the query method
    result = db.get_query_result(selector)

    # Create a list to store the documents
    data_list = []

    # Iterate through the results and add documents to the list
    for doc in result:
        data_list.append(doc)

    # Return the data as JSON
    return JsonResponse(data_list)


def post_review(request):
    """Post a new review."""

    # Check if the request body is empty
    if not request.json:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

    # Extract review data from the request JSON
    review_data = request.json

    # Validate that the required fields are present in the review data
    required_fields = ["id", "name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"]
    for field in required_fields:
        if field not in review_data:
            return JsonResponse({"error": f"Missing required field: {field}"}, status=400)

    # Save the review data as a new document in the Cloudant database
    db.create_document(review_data)

    # Return a success response
    return JsonResponse({"message": "Review posted successfully"}, status=201)