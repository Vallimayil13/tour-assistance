import wikipedia
from transformers import pipeline
from flask import Flask, request, jsonify
from gtts import gTTS
import os
import re
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize the Hugging Face Question Answering pipeline
qa_pipeline = pipeline("question-answering")

# Create static directory if it doesn't exist
if not os.path.exists("static"):
    os.makedirs("static")

# Function to fetch Wikipedia content based on the question
def get_wikipedia_content(question):
    try:
        # Extract the site name from the question
        site_name = extract_site_name_from_question(question)
        
        # Search for the heritage site on Wikipedia
        search_results = wikipedia.search(site_name, results=1)
        
        if search_results:
            page = wikipedia.page(search_results[0])  # Get the first result page
            content = page.content

            # Just return the visible content from the page
            return content
        else:
            return "Sorry, I couldn't find any relevant information on that topic."
    except Exception as e:
        return "Sorry, there was an error while fetching the information."

# Function to extract the site name from the question
def extract_site_name_from_question(question):
    # Clean the question to extract the relevant site name
    keywords = ["where", "about", "built", "located"]
    for keyword in keywords:
        question = question.replace(keyword, '')
    return question.strip()

# Function to extract the answer from the content using the Hugging Face QA model
def extract_answer(question, context):
    try:
        # Using the Hugging Face pipeline to extract the answer
        result = qa_pipeline({
            'question': question,
            'context': context
        })
        return result['answer']
    except Exception as e:
        return "Sorry, I couldn't extract the answer."

# API endpoint to handle user questions
@app.route("/ask", methods=["POST"])
def ask_question():
    question = request.json.get("question")  # Get the question from the front-end
    
    # Fetch the relevant Wikipedia content based on the question
    context = get_wikipedia_content(question)
    
    if context == "Sorry, I couldn't find any relevant information on that topic.":
        return jsonify({"answer": context, "audio_path": None})
    
    # Extract the answer from the context using the advanced QA model
    answer = extract_answer(question, context)
    
    # Generate TTS (Text-to-Speech) for the answer
    tts = gTTS(text=answer, lang='en')
    audio_file_path = "static/response.mp3"  # Define the path to save the audio file
    tts.save(audio_file_path)

    # Return the response and the audio file path
    return jsonify({"answer": answer, "audio_path": audio_file_path})

if __name__ == "__main__":
    app.run(debug=True)

