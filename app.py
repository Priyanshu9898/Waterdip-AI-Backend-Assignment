from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from dotenv import load_dotenv
import os
from pymongo.errors import PyMongoError

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get MongoDB URI from environment variables
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

@app.route("/")
def Home():
    return "<h1>Hello world</h1>"


@app.route("/v1/task", methods=["POST"])
def create_task():
    if(request.method == "POST"):
        try:
            res = mongo.db.task.insert_one({"title": request.json['title'], "isTaskCompleted": False})
            return jsonify({"id": str(res.inserted_id)}), 201
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


