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
    # Extract email and password from form data
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logout route to destroy the user session
    Returns:
        Response: The response with appropriate status and redirection
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


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
    user_request = request.form
    user_email = user_request.get('email', '')
    is_registered = AUTH.create_session(user_email)
    if not is_registered:
        abort(403)
    token = AUTH.get_reset_password_token(user_email)
    return jsonify({"email": user_email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Update user password based on the reset_token provided.

    This endpoint expects a PUT request with form data containing:
    - email: User's email address
    - reset_token: Token to validate the password reset request
    - new_password: The new password to be set

    If the reset_token is valid, the user's password is updated,
    and a JSON response with a success message is returned.
    If the reset_token is invalid, a 403 HTTP response is returned.

    Returns:
        JSON: {"email": "<user email>", "message": "Password updated"}
              or {"message": "Invalid reset token"}, HTTP status code 403
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)

    return jsonify({'email': email, 'message': 'Password updated'}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
