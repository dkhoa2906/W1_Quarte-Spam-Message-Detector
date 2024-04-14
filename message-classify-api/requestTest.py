import requests

# URL of your Flask server
url = 'http://127.0.0.1:5000/'  # Update this with your server's URL if necessary

# Message to classify
message = {
    'text': 'This is a spam message. Click here to win a million dollars!'
}

# Send POST request
response = requests.post(url, json=message)

# Check response
if response.status_code == 200:
    data = response.json()
    print("Prediction:", data['prediction'])
else:
    print("Error:", response.text)
