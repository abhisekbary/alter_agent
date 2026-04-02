# importing libraries
import requests
import os

# load environment variables
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

# utility function to send push notifications
def send_push_notification(message, title='You have a new notification from Alter Agent !'):
    url = "https://api.pushover.net/1/messages.json"
    payload = {'user': PUSHOVER_USER, 'token': PUSHOVER_TOKEN, 'title': title, 'message': message}
    response = requests.post(url, data=payload)
    return response.status_code == 200