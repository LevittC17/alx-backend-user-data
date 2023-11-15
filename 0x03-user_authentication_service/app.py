#!/usr/bin/env python3

"""
Basic Flask app
"""


from flask import Flask, request, jsonify
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
