const { create } = require('apisauce');
const dotenv = require('dotenv');

// Load environment variables from .env file
dotenv.config();

// Airtable API credentials
const AIRTABLE_PERSONAL_ACCESS_TOKEN = process.env.AIRTABLE_PERSONAL_ACCESS_TOKEN;
const AIRTABLE_BASE_ID = process.env.AIRTABLE_BASE_ID;
const CUSTOMERS_TABLE_ID = process.env.CUSTOMERS_TABLE_ID;
const DRIVERS_TABLE_ID = process.env.DRIVERS_TABLE_ID;

// Airtable API endpoint
const AIRTABLE_CUSTOMERS_ENDPOINT = `https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/${CUSTOMERS_TABLE_ID}`;
const AIRTABLE_DRIVERS_ENDPOINT = `https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/${DRIVERS_TABLE_ID}`;

const api = create({
    baseURL: AIRTABLE_CUSTOMERS_ENDPOINT,
    headers: {
        "Authorization": `Bearer ${AIRTABLE_PERSONAL_ACCESS_TOKEN}`,
        "Content-Type": "application/json"
    }
});



async function registerUser() {
    const firstName = "First Name";
    const lastName = "Last Name";
    const email = "Email";
    const phoneNumber = "09064531233";
    const currentLocation = "Zoo";

    const data = {
        "fields": {
            "First Name": firstName,
            "Last Name": lastName,
            "Email": email,
            "Phone Number": phoneNumber,
            "Current Location": currentLocation
        }
    };
        
    // start making calls
    api
    .post('', data)
    .then(response => response.ok)
    .then(console.log)

    
}

// Example usage
registerUser();
