import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    EMERGENCY_API_KEY = os.getenv("EMERGENCY_API_KEY", "your-emergency-api-key")
    TWILIO_SID = os.getenv("TWILIO_SID", "your-twilio-sid")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your-twilio-auth-token")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "your-twilio-phone-number")
