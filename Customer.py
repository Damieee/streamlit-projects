import streamlit as st
import requests
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()

load_dotenv(dotenv_path=dotenv_path)


# Airtable API credentials
AIRTABLE_PERSONAL_ACCESS_TOKEN = os.getenv("AIRTABLE_PERSONAL_ACCESS_TOKEN")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
ORDERS_TABLE_ID = os.getenv("ORDERS_TABLE_ID")


# Airtable API endpoint
AIRTABLE_ENDPOINT = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{ORDERS_TABLE_ID}"

# Function to fetch data from Airtable
def fetch_data():
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}"
    }
    response = requests.get(AIRTABLE_ENDPOINT, headers=headers)
    data = response.json()
    return data.get('records', [])


# Function to update ride status
def update_ride_status(order_id, new_status):
    headers = {
        "Authorization": f"Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    # Find the record with the matching order_id
    record = next((r for r in fetch_data() if r['fields'].get('Order ID') == order_id), None)
    if record:
        record_id = record['id']
        order_id = record['fields']['Order ID']

        params = {
            "records": [
                {
                    "id": record_id,

                    "fields": {
                        "Order Status": new_status
                    }
                }
            ]
        }

        response = requests.patch(AIRTABLE_ENDPOINT, json=params, headers=headers)
        if response.status_code == 200:
            return True
        else:
            st.error(f"Failed to update ride status: {response.text}")
    else:
        st.error(f"No order found with ID {order_id}")

    return False


# Streamlit app
def OrderStatusMonitor():
    st.title("Glidee Customer Order Management ✈️")

    # Fetch data from Airtable
    data = fetch_data()

    # Display data and provide options
    if data:

        # Input field for order ID in the sidebar
        order_id = st.sidebar.text_input("Enter Order ID:")

        if order_id:

            order_details = {}
        else:
            order_details = {}

        for record in data:
            if record['fields']["Order ID"] == order_id:
                order_details = record['fields']

        # Allow user to check status or cancel ride
        st.sidebar.title(f"Select action for Order {order_id}:")
        action = st.sidebar.radio("", ["Check Status", "Cancel Ride"])

        if action == "Check Status":
            if st.sidebar.button("Check Order Status", key="order_status"):

                if order_details:
                    st.subheader("Order Details")
                    st.write(f"**Order ID:** {order_details['Order ID']}")
                    st.write(f"**Pickup Location:** {order_details['Pickup Location']}")
                    st.write(f"**Order Status:** {order_details['Order Status']}")
                    st.write(f"**Order Creation Time:** {order_details['Order Creation Time']}")
                    st.write("---")
                else:
                    st.write("Status:", order_details.get("Status", "Not Available"))

        elif action == "Cancel Ride":
            if st.sidebar.button("Confirm Cancellation", key="confirm_cancel"):
                if update_ride_status(order_id, "Cancelled"):
                    st.success("Ride cancelled successfully!")
                else:
                    st.error(f"Failed to cancel ride")
    else:
        st.write("No data available")

