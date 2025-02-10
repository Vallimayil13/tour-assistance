from app import app
from flask import jsonify, request, render_template
from models import HeritageSite
import requests  # Import for external API calls (EmergencyAPI.org)

# Define a Route for the Root ("/")
@app.route('/')
def home():
    # Render the homepage with clickable images of heritage sites
    return render_template('index.html')

# Route to fetch all heritage sites (used on the home page for clickable images)
@app.route('/heritage_sites', methods=['GET'])
def get_heritage_sites():
    sites = HeritageSite.get_all_sites()  # Assuming this method fetches all sites from the database or static data
    return jsonify(sites), 200

# Route to fetch a specific heritage site by name (used for detailed page)
@app.route('/heritage_sites/<string:name>', methods=['GET'])
def get_heritage_site(name):
    site = HeritageSite.get_site_by_name(name)  # Fetch the site by name from the model
    if site:
        return render_template('heritage_site.html', site=site)  # Render the detailed page with site data
    else:
        return jsonify({"error": "Heritage site not found"}), 404

# Route to handle emergency SOS
@app.route('/emergency', methods=['POST'])
def emergency_alert():
    data = request.get_json()
    location = data.get('location')  # Get location from the request
    
    if location:
        lat = location.get('lat')
        lon = location.get('lon')

        # Call the emergency API to get nearby emergency services
        emergency_services = get_emergency_services(lat, lon)

        # Send alerts to the emergency services (via email, SMS, or other methods)
        send_alert_to_services(emergency_services, lat, lon)

        return jsonify({"message": "Emergency alert sent successfully."}), 200
    return jsonify({"error": "Location data missing"}), 400

# Function to get emergency services based on location (using Emergency API)
def get_emergency_services(lat, lon):
    # Replace this with the actual EmergencyAPI.org endpoint you are using
    api_url = f'https://api.emergencyapi.org/v1/nearest?lat={lat}&lon={lon}&apikey=YOUR_API_KEY'
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json()  # Return the emergency services info (hospital, ambulance, police, etc.)
    else:
        return []  # Return an empty list if the API call fails

# Function to send an alert to the emergency services
def send_alert_to_services(emergency_services, lat, lon):
    # Here you would send the actual alert to the emergency services.
    # This could be an email, SMS (Twilio), or other communication methods.
    
    for service in emergency_services:
        service_name = service.get("name", "Unknown Service")
        service_contact = service.get("contact", "Unknown Contact")

        # Print out the service information as a mock alert (for now)
        print(f"Sending alert to {service_name} at {service_contact} for user at location {lat}, {lon}")
        
        # You can implement real alerting functionality here (using Twilio, email, etc.)
        # For example, if using Twilio to send SMS, you'd call a Twilio function like:
        # send_sms(service_contact, lat, lon)

# Route to fetch nearby heritage sites based on user's location
@app.route('/nearby_sites', methods=['GET'])
def get_nearby_sites():
    user_location = request.args
    user_lat = float(user_location.get('lat', 0))
    user_lon = float(user_location.get('lon', 0))
    
    nearby_sites = HeritageSite.get_nearby_sites(user_lat, user_lon)  # This method should fetch nearby sites based on user location
    return jsonify(nearby_sites), 200

