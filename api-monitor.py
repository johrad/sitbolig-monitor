from python_graphql_client import GraphqlClient
import time
from datetime import datetime
import random
from playsound import playsound


def checkApartmentsAvail(AptToCheck):
    client = GraphqlClient(endpoint="https://as-portal-api-prodaede2914.azurewebsites.net/graphql") # found from inspect element

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
        "rentalObjectIds": AptToCheck, # checks the apt we want
        "showUnavailable": True,
        "reservationCode": "",
        "includeFilterCounts": False
        }}

    json_data = client.execute(query=query, variables=variables)
    data = json_data['data']['housings']['housingRentalObjects']
    return data[0]['isAvailable'] #filters so only a boolean.

# list of apt to check
AptToCheck = ["HK46-41", "OB043-103", "HK15-33", "MAG2-22"]

# init logfile name
log_file = 'website_update_log_MONITOR.txt'

while True:
    try:
        for apartment in AptToCheck:
            time.sleep(random.randint(4, 11))
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if checkApartmentsAvail(apartment):
                message = f"{current_timestamp}: {apartment} is available !!!!!"
                
                print(message)

                with open(log_file, 'a') as file:
                    file.write(message + '\n')

                playsound('alarm1.wav')

            else:
                 print(f"Refreshed {apartment} at {current_timestamp}")


    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        with open(log_file, 'a') as file:
                    file.write(error_message + ' !!!!!!!!! \n')
        playsound('pling.wav') # wake up if errors

    time.sleep(random.randint(60, 100)) # tune if need be