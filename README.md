# Waterdip-AI-Backend-Assignment
Waterdip AI Backend Assignment

# Project Description

This project is a simple Flask application that uses MongoDB as its database. It implements a Task API where you can add, get, update, and delete tasks. Tasks have a title and a is_completed property.

## Getting Started

### Prerequisites

The project uses **Python 3.7** or higher. The required libraries are listed in the `requirements.txt` file including flask, pymongo, and pytest for testing.

Also, make sure you have MongoDB installed and running on your machine, or a MongoDB Atlas account.

### Installing & Setting Up Environment Variables

1. Clone the repository to your local machine

    ```
    git clone https://github.com/Priyanshu9898/Waterdip-AI-Backend-Assignment

2. Navigate to the project directory and install the required packages

    ```
    cd Waterdip-AI-Backend-Assignment pip install -r requirements.txt

3. Create a `.env` file in your root directory and add the following

    ```
    MONGO_URI=mongodb://localhost:27017/myDatabase

### Running the Application Without MongoDB Database 

1. Navigate back to the root directory and execute the following command to run the server:

    ```
    python app.py
    
### Running the Application With MongoDB Database 

1. Navigate back to the root directory and execute the following command to run the server:

    ```
    python TaskManagerMongoDB.py

## Testing

This application includes a pytest testing suite. To run the tests, navigate to the root directory and execute:

    
    pytest Test.py

## API Endpoints

- `GET /v1/tasks`: Fetches all the tasks.
- `POST /v1/tasks`: Creates one or multiple tasks. Accepts a JSON body.
- `GET /v1/tasks/<id>`: Fetches the task with the given id.
- `PUT /v1/tasks/<id>`: Updates the task with the given id. Accepts a JSON body.
- `DELETE /v1/tasks/<id>`: Deletes the task with the given id.
- `DELETE /v1/tasks`: Deletes multiple tasks. Accepts a JSON body.

## Error Handling

If an error occurs during a database operation, PyMongoError will be caught, an error message will be shown and server responds with a status code 500. If the provided id is not valid, InvalidId will be caught and returns a status code 400.

## Contact

For more information, please contact - priyanshumalaviya9210@gmail.com
