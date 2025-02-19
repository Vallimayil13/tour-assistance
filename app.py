from flask import Flask, jsonify, request, render_template  # Import render_template
from flask_cors import CORS
from pymongo import MongoClient
import openai
import requests  # For emergency notifications like Twilio, email, etc.
from google.cloud import speech
from google.cloud import texttospeech
import os
from views import emergency_blueprint  # Import the blueprint from views.py

# Flask app setup
app = Flask(__name__)
CORS(app)

# Register the emergency blueprint
app.register_blueprint(emergency_blueprint)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
db = client['heritage_sites_db']
collection = db['heritage_sites']

# OpenAI API setup (Replace with your OpenAI API key)
openai.api_key = "your-openai-api-key"

# Google Cloud Speech-to-Text and Text-to-Speech Setup (Ensure you have Google Cloud SDK set up)
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Define Root Route to render HTML
@app.route('/')
def home():
    # This will render index.html from the templates folder
    return render_template('index.html')

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

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
