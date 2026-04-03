# importing necessary libraries
from openai import OpenAI
from pypdf import PdfReader
import yaml
import json
import gradio as gr
from src.utils.utils import send_push_notification
from src.tools.tools import tools, tool_registry
from src.config.config import settings

# creating the chat agent class
class ChatAgent:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model_name = settings.model_name
        self.prompt_file = settings.prompt_file
        self.user = settings.user
        self.user_role = settings.user_role
        self.user_linkedin_profile = settings.user_linkedin_profile
        self.user_professional_summary = settings.user_professional_summary
        self.prompts = self.load_prompts()
        self.system_prompt = self.create_system_prompt()

    # function to load user linkedin profile and professional summary
    def load_user_details(self):
        professional_summary, linkedin_profile = None, ''

        # loading professional summary
        with open(self.user_professional_summary, 'r') as file:
            professional_summary = yaml.safe_load(file)
            professional_summary = yaml.dump(professional_summary,sort_keys=False)

        # loading linkedin profile
        reader = PdfReader(self.user_linkedin_profile)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                linkedin_profile += text + "\n"

        return professional_summary, linkedin_profile

    # function to load prompts from yaml file
    def load_prompts(self):
        # loading prompts
        with open(self.prompt_file, 'r') as file:
            prompts = yaml.safe_load(file)

        # loading user details
        professional_summary, linkedin_profile = self.load_user_details()
        
        # formatting prompts with user details
        system_prompt = prompts['system_prompt']
        alter_ego_prompt = system_prompt['alter_ego'].format(user=self.user, user_role=self.user_role)
        rejection_message = system_prompt['rejection_message'].format(user=self.user)
        summary = system_prompt['summary'].format(user=self.user, summary=professional_summary)
        linkedin_profile = system_prompt['linkedin_profile'].format(user=self.user, linkedin_profile=linkedin_profile)

        return {
            'alter_ego_prompt': alter_ego_prompt,
            'rejection_message': rejection_message,
            'summary': summary,
            'linkedin_profile': linkedin_profile
        }
    
    # function to create system prompt
    def create_system_prompt(self):
        system_prompt = ''
        for prompt in self.prompts.values():
            system_prompt += prompt + "\n\n"
        
        return system_prompt
    
    # function to handle tool calls
    def handle_tool_calls(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if tool_name in tool_registry:
                tool_func = tool_registry[tool_name]
                result = tool_func(**tool_args)
                results.append({'role': 'tool', 'content': json.dumps(result), 'tool_call_id': tool_call.id})

        return results
            

    # agentic loop
    def chat(self,message,history):
        messages = [{'role': 'system', 'content': self.system_prompt}] + history + [{'role': 'user', 'content': message}]
        done = False
        while not done:
            response = self.client.chat.completions.create(model=self.model_name, messages=messages, tools = tools, tool_choice='auto')
            finish_reason = response.choices[0].finish_reason
            
            if finish_reason == 'tool_calls':
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_calls(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True

        return response.choices[0].message.content

if __name__ == "__main__":
    agent = ChatAgent()
    gr.ChatInterface(agent.chat, type="messages").launch()