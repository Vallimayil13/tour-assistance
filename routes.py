from app import app
from flask import jsonify, request
from models import HeritageSite

# Define a Route for the Root ("/")
@app.route('/')
def home():
    return "Welcome to the Heritage Site API!"

# Route to fetch all heritage sites
@app.route('/heritage_sites', methods=['GET'])
def get_heritage_sites():
    sites = HeritageSite.get_all_sites()
    return jsonify(sites), 200

# Route to fetch a specific heritage site by name
@app.route('/heritage_sites/<string:name>', methods=['GET'])
def get_heritage_site(name):
    site = HeritageSite.get_site_by_name(name)
    if site:
        return jsonify(site), 200
    else:
        return jsonify({"error": "Heritage site not found"}), 404

# Route to handle emergency SOS
@app.route('/emergency', methods=['POST'])
def emergency_alert():
    data = request.get_json()
    location = data.get('location')
    if location:
        message = f"Emergency Alert: User at location {location['lat']}, {location['lon']} needs help."
        # In a real scenario, integrate with emergency services like SMS or email
        print(message)  # Mock behavior: printing the alert message for testing
        return jsonify({"message": "Emergency alert sent successfully."}), 200
    return jsonify({"error": "Location data missing"}), 400

# Route to fetch nearby heritage sites based on user's location
@app.route('/nearby_sites', methods=['GET'])
def get_nearby_sites():
    user_location = request.args
    user_lat = float(user_location.get('lat', 0))
    user_lon = float(user_location.get('lon', 0))
    
    nearby_sites = HeritageSite.get_nearby_sites(user_lat, user_lon)
    return jsonify(nearby_sites), 200
