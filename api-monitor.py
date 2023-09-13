from python_graphql_client import GraphqlClient
import json


def checkApartmentsAvail(aptToCheck):
    client = GraphqlClient(endpoint="https://as-portal-api-prodaede2914.azurewebsites.net/graphql")

    query = """
    query GetHousingIds($input: GetHousingsInput!) {
    housings(filter: $input) {
        housingRentalObjects {
        rentalObjectId
        isAvailable
        hasActiveReservation
        }}}

    """
    variables = {
        "input":{
        "rentalObjectIds": toCheck,
        "showUnavailable": True,
        "reservationCode": "",
        "includeFilterCounts": False
        }}

    json_data = client.execute(query=query, variables=variables)
    data = json_data['data']['housings']['housingRentalObjects']

    return data[0]['isAvailable']

toCheck = ["HK46-41"]