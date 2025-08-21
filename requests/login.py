import requests
import json

# URL you want to send the POST request to
url = "http://127.0.0.1:8000/login/login/"

# Data to send (JSON format)
data = {
    "username": "yash31166",
    "password": "StrongPass@123"
}

# Send POST request
response = requests.post(url, json=data)

# Print status code
print("Status Code:", response.status_code)

# Pretty-print JSON response
try:
    response_json = response.json()
    print("Response Body:")
    print(json.dumps(response_json, indent=4))  # Pretty print with 4-space indentation
except ValueError:
    print("Response Body is not JSON:")
    print(response.text)
