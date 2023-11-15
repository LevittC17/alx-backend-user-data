#!/usr/bin/env python3

"""
Basic Flask app
"""


from flask import Flask, request, jsonify, make_response, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """
    Method to return json
    """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    Register a new user
    Expects form data fields: 'email' and 'password'
    Responds with a JSON payload indicating success or failure
    Returns:
        JSON: {'email': '<registered email>', 'message': 'user created'}
               or
              {'message': 'email already registered'}
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        return jsonify({"message": "Missing email or password"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": str(e)}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles the login endpoint (POST /sessions)

    Expects form data with 'email' and 'password' fields
    If the login information is correct, create new session for the user
    Returns:
        JSON payload with user email and a success message
    If login info is incorrect, return a 401 Unauthorized response
    If any other exception occurs, it returns a 400 Bad Request response
    Returns:
        Response: Flask response object
    """
    try:
        # Extract email and password from form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if login information is correct
        user = AUTH.valid_login(email, password)
        if user:
            # Create a new session and set session_id as a cookie in
            # the response
            session_id = AUTH.create_session(email)
            response = jsonify({'email': email, 'message': 'logged in'})
            response.set_cookie('session_id', session_id)
            return response
        else:
            # Unauthorized if login information is incorrect
            abort(401)
    except Exception as e:
        # Bad request if any other exception occurs
        return make_response(jsonify({'message': str(e)}), 400)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
