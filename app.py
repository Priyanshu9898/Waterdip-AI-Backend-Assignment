from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get MongoDB URI from environment variables
app.config['MONGO_URI'] = os.getenv('MONGO_URI')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


