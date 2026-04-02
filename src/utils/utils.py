# importing libraries
import requests
from src.config.config import settings

# utility function to send push notifications
def send_push_notification(message, title='You have a new notification from Alter Agent !'):
    url = settings.pushover_url
    user = settings.pushover_user
    token = settings.pushover_token
    payload = {'user': user, 'token': token, 'title': title, 'message': message}
    response = requests.post(url, data=payload)
    return response.status_code == 200