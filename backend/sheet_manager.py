from database_interface import *
import json

def store_sheet(user_id, sheet_data):
    sheet_type = sheet_data["type"]
    sheet_id = sheet_data["sheet_id"]
    print(sheet_id)
    save_data = json.dumps(sheet_data)

    if sheet_id == "new":
        return insert_sheet(user_id, sheet_type, save_data)
    else:
        return sheet_id if update_sheet(user_id, sheet_id, sheet_type, save_data) else None

def load_sheet_list(user_id):
    print("Function called")
    return get_sheets_from_database(user_id) 

def load_sheet(user_id, sheet_id):
    row = get_sheet_from_database(user_id, sheet_id)

    if row is None:
        return {
            "success": False,
            "message": "Sheet not found.",
            "status": 404
        }
    
    try:
        saved_data = json.loads(row["data"])

    except json.JSONDecodError:
        return {
            "success": False,
            "message": "The saved sheet data is invalid.",
            "status": 500
        }

    return {
        "success": True,
        "sheet": {
            "sheet_id": row["id"],
            "sheet_type": row["type"],
            "data": saved_data
        },
        "status":200
    }
