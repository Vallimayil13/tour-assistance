from flask import Blueprint, jsonify, request
import requests  # To send HTTP requests to the EmergencyAPI and Twilio
from twilio.rest import Client

# Create a blueprint for organizing routes in separate files
emergency_blueprint = Blueprint('emergency', __name__)

# Your Twilio credentials
TWILIO_SID = 'your_twilio_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# Emergency API setup (https://emergencyapi.org)
EMERGENCY_API_KEY = 'your_emergency_api_key'  # Replace with your real API key

# Route to handle emergency alerts dynamically
@emergency_blueprint.route('/emergency', methods=['POST'])
def emergency_alert():
    data = request.get_json()  # Retrieve JSON data from the request
    location = data.get('location')

    if location:
        lat = location['lat']
        lon = location['lon']

        # Step 1: Get nearby emergency services using the Emergency API
        nearby_services = get_nearby_emergency_services(lat, lon)

        if nearby_services:
            # Step 2: Send an emergency alert via Twilio to the nearest service
            emergency_contact_number = nearby_services[0]['phone']  # Choose the first service for simplicity
            message = f"Emergency Alert: User at location {lat}, {lon} needs help."
            send_emergency_alert(message, emergency_contact_number)

            return jsonify({"message": "Emergency alert sent successfully."}), 200
        else:
            return jsonify({"error": "No nearby emergency services found."}), 404

    return jsonify({"error": "Location data missing"}), 400


# Function to call EmergencyAPI to get nearby emergency services
def get_nearby_emergency_services(lat, lon):
    url = f'https://api.emergencyapi.org/v1/services?lat={lat}&lon={lon}'
    headers = {'Authorization': f'Bearer {EMERGENCY_API_KEY}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        services = response.json()
        return services  # Return list of services
    else:
        print("Error fetching emergency services:", response.text)
        return None


# Function to send emergency alert using Twilio
def send_emergency_alert(message, contact_number):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    try:
        # Send an SMS message to the emergency contact using Twilio
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=contact_number
        )
        print("Emergency alert sent successfully.")
    except Exception as e:
        print(f"Failed to send emergency alert: {str(e)}")
