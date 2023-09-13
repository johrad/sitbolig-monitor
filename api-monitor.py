from python_graphql_client import GraphqlClient
import time
from datetime import datetime
import random
from playsound import playsound


def checkApartmentsAvail(AptToCheck):
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
        "rentalObjectIds": AptToCheck,
        "showUnavailable": True,
        "reservationCode": "",
        "includeFilterCounts": False
        }}

    json_data = client.execute(query=query, variables=variables)
    data = json_data['data']['housings']['housingRentalObjects']
    return data[0]['isAvailable']

AptToCheck = ["HK46-41", "OB043-103", "KL124-702"]

log_file = 'website_update_log_MONITOR.txt'

while True:
    try:
        for appartment in AptToCheck:
            time.sleep(random.randint(1, 3))
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if checkApartmentsAvail(appartment):
                message = f"{current_timestamp}: {appartment} is available !!!!!"
                
                print(message)

                with open(log_file, 'a') as file:
                    file.write(message + '\n')

                playsound('pling.wav')

            else:
                 print(f"Refreshed {appartment} at {current_timestamp}")


    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        with open(log_file, 'a') as file:
                    file.write(error_message + ' !!!!!!! \n')
        playsound('alarm1.wav')

    time.sleep(random.randint(4, 10))