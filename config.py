import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")  # Default to localhost
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Use a secure secret key in production
