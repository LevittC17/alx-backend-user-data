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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logout route to destroy the user session
    Returns:
        Response: The response with appropriate status and redirection
    """
    session_id = request.cookies.get('session_id')

    if session_id is None:
        # No session ID provided in the request, respond with 403 Forbidden
        return make_response(jsonify({'message': 'Forbidden'}), 403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        # User found, destroy the session
        AUTH.destroy_session(user.id)

        # Redirect the user to GET /
        return redirect('/', code=302)
    else:
        # User not found, respond with 403 Forbidden
        return make_response(jsonify({'message': 'Forbidden'}), 403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """
    Profile route to retrieve user profile based on session ID.
    Returns:
        Response: The response with appropriate status and JSON payload.
    """
    session_id = request.cookies.get('session_id')

    if session_id is None:
        # No session ID provided in the request, respond with 403 Forbidden
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        # User found, respond with 200 OK and user profile JSON payload
        return jsonify({"email": user.email}), 200
    else:
        # User not found, respond with 403 Forbidden
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Get the reset password token for a user
    Request:
        POST /reset_password
        Form data: {'email': '<user email>'}
    Response:
        200 OK - {"email": "<user email>", "reset_token": "<reset token>"}
        403 Forbidden - {"message": "Email not registered"}
    """
    try:
        email = request.form.get('email')
        reset_token = AUTH.get_reset_password_toke(email)
        response_data = {'email': email, 'reset_token': reset_token}
        return jsonify(response_data), 200
    except ValueError:
        return jsonify({'message': 'Email not registered'}), 403


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
