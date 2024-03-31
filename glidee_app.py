import streamlit as st
import requests
from Customer import OrderStatusMonitor
from Driver import DriverMonitor
import re


# Airtable API credentials
AIRTABLE_PERSONAL_ACCESS_TOKEN = 'pat0bujZD5PIV5Apc.51bb880c298b9768dfcbc0e0326f94ad9d6b6b3b7d2b880486179f01d54168c5'
AIRTABLE_BASE_ID = 'app8pgQ8UWEiusMHE'
TABLE_ID = 'tblLY6iolwFQ7sCXG'


# Airtable API endpoint
AIRTABLE_ENDPOINT = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{TABLE_ID}"

# Function to fetch data from Airtable
def fetch_data():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}"
    }
    response = requests.get(AIRTABLE_ENDPOINT, headers=headers)
    data = response.json()
    return data.get('records', [])

# Function to extract emails from records
def extract_emails(records):
    emails = []
    for record in records:
        fields = record.get('fields', {})
        email = fields.get('Email')
        if email:
            emails.append(email)
    return emails

# Fetch data from Airtable
records = fetch_data()

# Extract emails from records
emails = extract_emails(records)


def validate_email(email):
    # Regular expression for validating email addresses
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

def validate_phone_number(phone_number):
    # Regular expression for validating phone numbers
    pattern = r'^\d{10}$'  # Assuming a 10-digit phone number
    if re.match(pattern, phone_number):
        return True
    else:
        return False

def validate_current_location(current_location):
    # Simple validation, can be extended based on requirements
    if len(current_location) > 0:
        return True
    else:
        return False



# Function to handle user registration
def register_user():
    
    st.title("User Registration")
    user_type = st.radio("Are you a Customer or a Driver?", ("Customer", "Driver"))
    first_name = st.text_input("First Name *")
    last_name = st.text_input("Last Name *")
    email = st.text_input("Email *")
    phone_number = st.text_input("Phone Number *")
    current_location_options = ["Accord", "Zoo", "Harmony", "Peak Olam", "Camp"]
    current_location = st.selectbox("Current Location *", current_location_options)
    

    if st.button("Register"):

        if not first_name:
            st.error("First Name Field cannot be empty!")
            return
        if not last_name:
            st.error("Last Name Field cannot be empty!")
            return
        
        if email:
            if not validate_email(email):
                st.error("Please enter a valid email address!")
                return
            
        else:
            st.error("Email Field cannot be empty!")
            return
        
        if phone_number:
            if not validate_phone_number(phone_number):
                st.error("Please enter a valid phone number!")
                return
        else:
            st.error("Phone number Field cannot be empty!")
            return

        if not validate_current_location(current_location):
            st.error("Please enter your current location!")
            return

        
        # Prepare data payload
        data = {
            "user_type": user_type,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": phone_number,
            "location": current_location
        }
        # Make HTTP POST request to Zapier webhook URL
        response = requests.post("https://hooks.zapier.com/hooks/catch/18001983/3xn808b/", json=data)

        if response.status_code == 200:
            st.success(f"Registration successful as {user_type}!")
        else:
            st.error("Failed to register user. Please try again.")


# Function to handle order placement
def place_order():
    st.title("Place Order")

    email = st.text_input("Email *")
    pickup_location_options = ["Accord", "Zoo", "Harmony", "Peak Olam", "Camp"]
    pickup_location = st.selectbox("Pickup Location *", pickup_location_options)

    
    if st.button("Place Order"):

        if email:
            if not validate_email(email):
                st.error("Please enter a valid email address!")
                return
            if email not in emails:
                st.error(f"The email ({email}) does not exist in our database! Please enter the email address you registered with!")
                return
        else:
            st.error("Email Field cannot be empty!")
            return

        if not validate_current_location(pickup_location):
            st.error("Please enter your Pickup location!")
            return


        # Prepare data payload
        data = {

            "email": email,
            "pickup_location": pickup_location
        }

        # Make HTTP POST request to Zapier webhook URL
        response = requests.post("https://hooks.zapier.com/hooks/catch/18001983/3x74eeu/", json=data)

        if response.status_code == 200:
            st.success("Order placed successfully!")
        else:
            st.error("Failed to place order. Please try again.")

def main():
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.radio("Go to", ("Register User", "Place Order", "Customer? Manage ride status and cancellations", "Driver? Manage (Accept and Complete) Rides here"))

    if selected_page == "Register User":
        register_user()
    elif selected_page == "Place Order":
        place_order()
    elif selected_page == "Customer? Manage ride status and cancellations":
        OrderStatusMonitor()
    elif selected_page == "Driver? Manage (Accept and Complete) Rides here":
        DriverMonitor()


if __name__ == "__main__":
    main()
