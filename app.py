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

# Create a Task
@app.route("/v1/tasks", methods=["POST"])
def create_task():
    if (request.method == "POST"):
        try:
            is_completed = request.json.get('is_completed', False)
            res = mongo.db.task.insert_one(
                {"title": request.json['title'], "is_completed": is_completed})
            return jsonify({"id": str(res.inserted_id)}), 201
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500


# Get all tasks
@app.route("/v1/tasks", methods=["GET"])
def get_tasks():
    if request.method == "GET":
        try:
            allTasks = []
            for doc in mongo.db.task.find():
                allTasks.append({"id": str(ObjectId(
                    doc['_id'])), "title": doc["title"], "is_completed": doc["is_completed"]})
            return jsonify({"tasks": allTasks}), 200

        except PyMongoError as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
