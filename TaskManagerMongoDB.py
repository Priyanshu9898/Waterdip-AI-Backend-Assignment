from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from dotenv import load_dotenv
import os
from pymongo.errors import PyMongoError
from bson.errors import InvalidId

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get MongoDB URI from environment variables
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)


@app.route("/")
def Home():
    return "<h1>Hello world</h1>"

# Create a single task or in bulk
@app.route("/v1/tasks", methods=["POST"])
def create_task():
    if request.method == "POST":

        data = request.get_json()

        if data is None:
            return jsonify({"error": "Invalid JSON data in the request"}), 400

        if data.get("tasks") is None:
            try:
                is_completed = data.get('is_completed', False)
                res = mongo.db.task.insert_one(
                    {"title": data['title'], "is_completed": is_completed})
                return jsonify({"id": str(res.inserted_id)}), 201
            except PyMongoError as e:
                return jsonify({'error': str(e)}), 500

        else:
            try:
                tasks = data['tasks']
                ids = []
                for task in tasks:
                    is_completed = task.get('is_completed', False)
                    doc = mongo.db.task.insert_one(
                        {"title": task['title'], "is_completed": is_completed})
                    ids.append(str(doc.inserted_id))

                return jsonify({"tasks": ids}), 201

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


# Get task by Id
@app.route("/v1/tasks/<id>", methods=["GET"])
def get_task(id):
    if request.method == "GET":
        try:
            doc = mongo.db.task.find_one({"_id": ObjectId(id)})

            if (doc is None):
                return jsonify({'error': 'There is no task at that id'}), 404
            else:
                return jsonify({"id": str(ObjectId(doc["_id"])), "title": doc["title"], "is_completed": doc["is_completed"]})

        except InvalidId as e:
            return jsonify({'error': 'Invalid id format'}), 400

        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500

# Update task by Id


@app.route("/v1/tasks/<id>", methods=['PUT'])
def update_task(id):
    if request.method == "PUT":
        try:
            existed_task = mongo.db.task.find_one({"_id": ObjectId(id)})

            if (existed_task is not None):

                title = request.json.get("title", existed_task['title'])
                is_completed = request.json.get(
                    "is_completed", existed_task['is_completed'])

                mongo.db.task.update_one({"_id": ObjectId(id)}, {'$set': {'title': title,
                                                                          'is_completed': is_completed
                                                                          }
                                                                 })
                return jsonify({}), 204
            else:
                return jsonify({"error": "There is no task at that id"}), 404

        except InvalidId as e:
            return jsonify({'error': 'Invalid id format'}), 400
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500


# Delete task by Id
@app.route("/v1/tasks/<id>", methods=["DELETE"])
def delete_task(id):
    if request.method == "DELETE":
        try:

            existed_task = mongo.db.task.find_one({"_id": ObjectId(id)})

            if (existed_task is not None):

                mongo.db.task.delete_one({"_id": ObjectId(id)})
                return jsonify({}), 204

            else:
                return jsonify({"error": "There is no task at that id"}), 404

        except InvalidId as e:
            return jsonify({'error': 'Invalid id format'}), 400
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500


# Delete task in bulk
@app.route('/v1/tasks', methods=['DELETE'])
def delete_multiple_tasks():
    try:
        data = request.get_json()

        for task in data['tasks']:
            mongo.db.task.delete_one({"_id": ObjectId(task['id'])})

        return jsonify({}), 204
    
    except PyMongoError as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
