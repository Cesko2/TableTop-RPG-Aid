from flask import Flask, jsonify, request
from flask_cors import CORS
from user_authentication import authenticate_user

app = Flask(__name__)
CORS(app)

# Listen for requests from frontend
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    
    # If request is empty throw error
    if data is None:
        return jsonify({
            "success": False,
            "message": "Request body must contain a JSON."
        }), 400

    username = data.get("username")
    password = data.get("password")

    # If missing data throw error
    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username and password are both required."
        }), 400

    # push data to user authenticator file
    result = authenticate_user(username, password)

    if result["success"]:
        return jsonify(result), 200

    # Default return
    return jsonify(result), 401

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
