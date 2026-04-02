# importing necessary libraries
from openai import OpenAI
import os
import json
from src.utils.utils import send_push_notification
from src.tools.tools import record_user_details, record_unknown_question, tools


send_push_notification('this is a test notification from Alter Agent !','Test Notification')