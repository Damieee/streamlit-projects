import requests
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()

load_dotenv(dotenv_path=dotenv_path)


# Airtable and Zapier API credentials
AIRTABLE_PERSONAL_ACCESS_TOKEN = os.getenv("AIRTABLE_PERSONAL_ACCESS_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
CUSTOMERS_TABLE_ID = os.getenv("CUSTOMERS_TABLE_ID")
DRIVERS_TABLE_ID = os.getenv("DRIVERS_TABLE_ID")


# Airtable API endpoint
AIRTABLE_CUSTOMERS_ENDPOINT = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{CUSTOMERS_TABLE_ID}"
AIRTABLE_DRIVERS_ENDPOINT = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{DRIVERS_TABLE_ID}"

def register_user():
    first_name = "First Name"
    last_name = "Last Name"
    email = "Email"
    phone_number = "09064531233"
    current_location = "Zoo"
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}"
    }
    # Prepare data payload
    data = {
        "fields": {
            "First Name": first_name,
            "Last Name": last_name,
            "Email": email,
            "Phone Number": phone_number,
            "Current Location": current_location
        }
    }

    try:
        response = requests.post(AIRTABLE_CUSTOMERS_ENDPOINT, json=data, headers=headers)
        
        # Check the response status code
        if response.status_code in [200, 201]:
            print("Registration successful!")
        else:
            # Raise an HTTPError if the status code indicates a failure
            response.raise_for_status()
            
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print the HTTP error
        print(f"Response content: {response.content}")  # Print the response content
    except Exception as err:
        print(f"An error occurred: {err}")

# Example usage
register_user()