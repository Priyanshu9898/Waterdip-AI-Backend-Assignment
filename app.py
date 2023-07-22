from flask import Flask, jsonify, request

app = Flask(__name__)
tasks = []
id_counter = 1


# Create a single task or in bulk
@app.route("/v1/tasks", methods=["POST"])
def create_task():
    global id_counter
    if request.method == "POST":

        data = request.get_json()

        tasks_to_create = []

        if data is None:
            return jsonify({"error": "Invalid JSON data in the request"}), 400

        if data.get("tasks") is None:

            if 'title' not in data:
                return jsonify({'error': 'Missing task title'}), 400

            data['id'] = id_counter

            if (data.get('is_completed') is None):
                data['is_completed'] = False

            tasks_to_create.append(data)
            id_counter += 1

            tasks.extend(tasks_to_create)
            created_ids = {'id': data['id']}
           
            return jsonify({"id": data['id']}), 201

        else:
            tasks_data = data['tasks']

            for task_data in tasks_data:

                if 'title' not in task_data:
                    return jsonify({'error': 'Missing task title'}), 400

                task_data['id'] = id_counter
                if (task_data.get('is_completed') is None):
                    task_data['is_completed'] = False

                tasks_to_create.append(task_data)
                id_counter += 1

            tasks.extend(tasks_to_create)
            created_ids = {'ids': [task['id'] for task in tasks_to_create]}
            return jsonify(created_ids), 201


@app.route('/v1/tasks', methods=['GET'])
def list_all_tasks():
    try:
        return jsonify({'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        for task in tasks:
            if task['id'] == task_id:
                return jsonify(task), 200

        return jsonify({'error': 'There is no task at that id'}), 404

    except Exception as e:
        return jsonify({'error': 'Unexpected error occurred'}), 500



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
