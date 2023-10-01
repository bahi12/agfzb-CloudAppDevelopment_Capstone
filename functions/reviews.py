import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def main(dict):
    authenticator = IAMAuthenticator('ZYiv6q8przFhNmxJSWs5DqjrHKgCE9vEsrx_aGEOrwuo')
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://c7414ad6-c35f-46d0-ad48-ba9c5933788f-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(db='reviews', document=dict['review']).get_result()
    DB_NAME = "reviews"
    print(DB.NAME.get_query_result)
    try:
        result_by_filter = DB_NAME.get_query_result(selector="review", raw_result=True)
        result = {
            'headers': {'Content-Type': 'application/json'},
            'body': {'data': response}
        }
        return result
    except Exception as e:
        print(f"Something went wrong: {e}")
        return {}

if __name__ == "__main__":
    dict = {"id":15}
    response = main(dict)
    print(response)