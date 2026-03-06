import json
import uuid
from datetime import datetime


# -------- JSON Helpers --------

def to_json(data):
    """
    Convert python object to JSON string
    """
    try:
        return json.dumps(data)
    except Exception as e:
        return {"error": str(e)}


def from_json(data):
    """
    Convert JSON string to python object
    """
    try:
        return json.loads(data)
    except Exception as e:
        return {"error": str(e)}


# -------- ID Generator --------

def generate_id():
    """
    Generate unique ID
    """
    return str(uuid.uuid4())


# -------- Timestamp --------

def current_timestamp():
    """
    Get current timestamp
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# -------- Response Formatter --------

def success_response(data):
    return {
        "status": "success",
        "data": data,
        "timestamp": current_timestamp()
    }


def error_response(message):
    return {
        "status": "error",
        "message": message,
        "timestamp": current_timestamp()
    }