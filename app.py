# importing necessary libraries
from openai import OpenAI
import os
import json
from dotenv import load_dotenv
from src.utils.utils import send_push_notification

# loading environment variables
load_dotenv(override=True)

# reading environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

# sending the push notification
send_push_notification(PUSHOVER_USER, PUSHOVER_TOKEN, "Hello, this is a test notification from Alter Agent!")