import streamlit as st
import requests

# Airtable API credentials
AIRTABLE_PERSONAL_ACCESS_TOKEN = 'pat0bujZD5PIV5Apc.51bb880c298b9768dfcbc0e0326f94ad9d6b6b3b7d2b880486179f01d54168c5'
AIRTABLE_BASE_ID = 'app8pgQ8UWEiusMHE'
ORDERS_TABLE_ID = 'tbl0fdZ87VI2WGrip'
CUSTOMERS_TABLE_ID = 'tblLY6iolwFQ7sCXG'
DRIVERS_TABLE_ID = 'tblBYefamOYeuLmIK'


# Airtable API endpoint
AIRTABLE_ORDER_ENDPOINT = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{ORDERS_TABLE_ID}"
AIRTABLE_DRIVER_ENDPOINT = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{DRIVERS_TABLE_ID}"

# Function to fetch data from Orders table in Airtable
def fetch_order_data():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}"
    }
    response = requests.get(AIRTABLE_ORDER_ENDPOINT, headers=headers)
    data = response.json()
    return data.get('records', [])

# Function to fetch data from Drivers table in Airtable

def fetch_driver_data():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}"
    }
    response = requests.get(AIRTABLE_DRIVER_ENDPOINT, headers=headers)
    data = response.json()
    return data.get('records', [])

# Function to update ride status
def update_ride_status(driver_email, order_id, new_status):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    # Find the record with the matching order_id
    record = next((r for r in fetch_order_data() if r['fields'].get('Order ID') == order_id), None)
    driver_record = next((r for r in fetch_driver_data() if r['fields'].get('Email') == driver_email), None)

    if record:
        record_id = record['id']
        order_id = record['fields']['Order ID']
        order_status = record['fields']['Order Status']

        if new_status == 'Accepted' and order_status != 'Pending':
            st.write('Sorry, you can no longer accept this order. This order has already been accepted.')
            return
        
        if new_status == 'Completed' and order_status != 'Accepted':
            st.write('Sorry, you can not complete this order if it was not previously accepted.')
            return


        driver_record_id = driver_record['id']

        params = {
            "records": [
                {
                    "id": record_id,

                    "fields": {
                        "Order Status": new_status,
                        "Driver Email": [driver_record_id],
                    }
                }
            ]
        }

        response = requests.patch(AIRTABLE_ORDER_ENDPOINT, json=params, headers=headers)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to update ride status: {response.text}")
    else:
        st.error(f"No order found with ID {order_id}")

    return False


# Streamlit app
def DriverMonitor():
    st.title("Glidee Driver Order Management 👮✈️")
    st.sidebar.title("Driver? Manage Rides here")


    # Fetch data from Airtable
    data = fetch_order_data()
    driver_data = fetch_driver_data()
    drivers_email_list = []
    order_id_list = []

    # Display data and provide options
    try:
        if driver_data:
            for record in driver_data:
                if record['fields']["Email"] != "":
                    drivers_email_list.append(record['fields']["Email"])
    except Exception as e:
        st.write(f"Error: {e}")
        return
    
    try:
        if data:
            for record in data:
                if record['fields']["Order ID"] != "":
                    order_id_list.append(record['fields']["Order ID"])

    except Exception as e:
        st.write(f"Error: {e}")


    if data:

        # Input field for order ID in the sidebar
        order_id = st.sidebar.text_input("Please Enter the Ride Order ID:")
        driver_email = st.sidebar.text_input("Driver? Please Enter your Email Address")

        if order_id and driver_email:

            order_details = {}
        else:
            order_details = {}

        if order_id in order_id_list:
            if driver_email in drivers_email_list:
                for record in data:
                    if record['fields']["Order ID"] == order_id:
                        order_details = record['fields']
            else:
                st.write("Sorry, This Driver does not exist is our Database")
                return
        else:
            st.write("Sorry, This Order does not exist in our Database")
            return
        
        # Allow Drivers to Accept or Complete Ride
        st.sidebar.title(f"Select action for Order {order_id}:")
        action = st.sidebar.radio("", ["Accept Ride", "Complete Ride"])

        if action == "Accept Ride":
            if st.sidebar.button("Accept Customer Order", key="accept_order"):

                if update_ride_status(order_id=order_id, driver_email=driver_email, new_status="Accepted"):
                    st.success("Ride Accepted successfully!")
                else:
                    st.error(f"Failed to Accept ride")

                if order_details:
                    st.subheader("Order Details")
                    st.write(f"**Order ID:** {order_details['Order ID']}")
                    st.write(f"**Pickup Location:** {order_details['Pickup Location']}")
                    
                    st.write("---")
                else:
                    st.write("Status:", order_details.get("Status", "Not Available"))

        elif action == "Complete Ride":
            if st.sidebar.button("Complete Customer Order", key="complete_order"):
                if update_ride_status(order_id=order_id, driver_email=driver_email, new_status="Completed"):
                    st.success("Ride completed successfully!")
                else:
                    st.error(f"Failed to complete ride")
    else:
        st.write("No data available")
