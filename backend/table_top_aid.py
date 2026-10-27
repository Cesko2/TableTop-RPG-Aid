from flask import Flask, jsonify, request, session
from flask_cors import CORS
from user_authentication import authenticate_user
from sheet_manager import *

app = Flask(__name__)
app.config.update(
    SECRET_KEY="development-key-replace-later",
    SESSION_COOKIE_NAME="session",
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE=None
)
CORS(app, origins=["http://localhost:35729"], supports_credentials=True)

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
        print("SETTING SESSION:", result["user_id"])
        session["user_id"] = result["user_id"]
        print(session["user_id"])
        return jsonify(result), 200

    # Default return
    return jsonify(result), 401

@app.route("/save_sheet", methods=["POST"])
def save_sheet():

    data = request.get_json(silent=True)
    user_id = session.get("user_id")

    sheet_id = store_sheet(user_id, data)

    return jsonify({ "success": True, "sheet_id": sheet_id }), 200

@app.route("/get_sheets", methods=["GET"])
def get_sheets():
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({
            "success": False,
            "message": "You are not signed in."
        }), 401

    rows = load_sheet_list(user_id)

    sheets = []
    
    for row in rows:
        saved_data = json.loads(row["data"])

        sheets.append({
            "sheet_id": row["id"],
            "sheet_type": row["type"],
            "name": saved_data.get("name"),
            "character_class": saved_data.get("class", "Class not specificed"),
            "level": saved_data.get("level", "Level not specificed")
        })

    return jsonify({
        "success": True,
        "sheets": sheets
    }), 200

@app.route("/get_sheet/<int:sheet_id>", methods=["GET"])
def get_sheet_route(sheet_id):
    user_id = session.get("user_id")

    if user_id is None:
        return jsonify({
            "success": False,
            "message": "You are not signed in."
        }), 401

    result = load_sheet(user_id, sheet_id)
    status = result.pop("status")

    return jsonify(result), status

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
