from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)  # Load configuration from config.py

# Enable CORS for cross-origin requests
CORS(app)

# MongoDB Connection
client = MongoClient(app.config['MONGO_URI'])
db = client['heritage_sites_db']
collection = db['heritage_sites']

# Import routes
from app import routes

