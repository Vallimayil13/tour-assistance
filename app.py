from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import openai
import requests  # For emergency notifications like Twilio, email, etc.
from google.cloud import speech
from google.cloud import texttospeech
import os

# Flask app setup
app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client['heritage_sites_db']
collection = db['heritage_sites']

# OpenAI API setup (Replace with your OpenAI API key)
openai.api_key = "your-openai-api-key"

# Google Cloud Speech-to-Text and Text-to-Speech Setup (Ensure you have Google Cloud SDK set up)
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Define Root Route
@app.route('/')
def home():
    return "Welcome to the Heritage Site API!"

# Route to process voice input (via STT) and retrieve data based on query
@app.route('/voice_query', methods=['POST'])
def process_voice_query():
    # Retrieve the audio file from the request (assumes audio file is sent via POST)
    audio_file = request.files['audio']
    
    # Convert audio to text using Google's Speech-to-Text API
    audio_content = audio_file.read()
    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    request = speech.RecognizeRequest(config=config, audio=audio)
    response = speech_client.recognize(request=request)

    # Extract text from the STT result
    text_query = response.results[0].alternatives[0].transcript if response.results else ""

    # Use OpenAI (LLM) to process the query and extract relevant keywords
    if text_query:
        keywords = extract_keywords_using_llm(text_query)
        # Use these keywords to query the MongoDB database
        data = query_heritage_sites_by_keywords(keywords)
        return jsonify(data), 200
    else:
        return jsonify({"error": "Could not understand the voice query."}), 400

# Function to extract keywords using OpenAI GPT
def extract_keywords_using_llm(query):
    prompt = f"Extract relevant keywords from the following query: {query}"
    response = openai.Completion.create(
        engine="text-davinci-003",  # or use another model of your choice
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )
    keywords = response.choices[0].text.strip().split(", ")
    return keywords

# Function to query MongoDB using extracted keywords
def query_heritage_sites_by_keywords(keywords):
    # Query database using the keywords (this is a simple example, you can improve logic)
    query = {"$or": [{"name": {"$regex": keyword, "$options": "i"}} for keyword in keywords]}
    sites = list(collection.find(query))
    
    # Format the MongoDB result
    for site in sites:
        site['_id'] = str(site['_id'])
    
    return sites

# Route to handle emergency alerts dynamically
@app.route('/emergency', methods=['POST'])
def emergency_alert():
    data = request.get_json()
    location = data.get('location')

    if location:
        message = f"Emergency Alert: User at location {location['lat']}, {location['lon']} needs help."

        # Sending emergency message via Twilio or any other service
        send_emergency_alert(message)

        return jsonify({"message": "Emergency alert sent successfully."}), 200
    return jsonify({"error": "Location data missing"}), 400

# Function to send emergency alert (Example using Twilio for SMS)
def send_emergency_alert(message):
    # Replace with real Twilio credentials and phone numbers
    twilio_sid = "your_twilio_sid"
    twilio_auth_token = "your_twilio_auth_token"
    twilio_phone_number = "your_twilio_phone_number"
    emergency_contact_number = "emergency_number_to_notify"

    # Send SMS using Twilio (example)
    client = requests.post(
        "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(twilio_sid),
        data={
            "From": twilio_phone_number,
            "To": emergency_contact_number,
            "Body": message,
        },
        auth=(twilio_sid, twilio_auth_token),
    )

    # Check response status
    if client.status_code == 201:
        print("Emergency alert sent successfully.")
    else:
        print("Failed to send emergency alert.")

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
