from src.utils.utils import send_push_notification

# tool: record_user_details
def record_user_details(email, name='Not provided', phone='Not provided', notes= 'No additional notes'):
    message = f"New user details recorded:\nName: {name}\nEmail: {email}\nPhone: {phone}\nNotes: {notes}"
    send_push_notification(message, title='New User Details Recorded')

    return {"status": "success", "message": "User details recorded and notification sent."}

record_user_details_json = {
    'name': 'record_user_details',
    'description': 'Use this tool to record that a user is interested in being in touch and provided an email address',
    'parameters': {
        'type': 'object',
        'properties': {
            'email': {
                'type': 'string',
                'description': 'The email address of the user'
            },
            'name': {
                'type': 'string',
                'description': 'The name of the user (optional)',
                'default': 'Not provided'
            },
            'phone': {
                'type': 'string',
                'description': 'The phone number of the user (optional)',
                'default': 'Not provided'
            },
            'notes': {
                'type': 'string',
                'description': 'Any additional notes about the user (optional)',
                'default': 'No additional notes'
            }
        },
        'required': ['email'],
        'additionalProperties': False
    }
}

# tool: record_unkonw_question
def record_unknown_question(question):
    send_push_notification(f"Recording unknown question: {question}", title="Unknown Question Recorded")
    return {"recorded": "ok"}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

# tool list to be passed to the agent
tools = [{"type": "function", "function": record_user_details_json},
         {"type": "function", "function": record_unknown_question_json}]