"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests
import json

with open("../../creds.json", "r") as f:
  creds = json.load(f)
#print(creds["COUCH_USERNAME"])
#print(creds["IAM_API_KEY"])

def main(creds):
    """Main Function

    Args:
        param_dict (Dict): input paramater

    Returns:
        _type_: _description_ TODO
    """

    try:
        
        client = Cloudant.iam(
            account_name=creds["COUCH_USERNAME"],
            api_key=creds["IAM_API_KEY"],
            connect=True,
        )
        print(f"Databases: {client.all_dbs()}")
    except CloudantException as cloudant_exception:
        print("unable to connect")
        return {"error": cloudant_exception}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
