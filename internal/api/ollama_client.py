from ollama import Client

class OllamaAPI:
    def __init__(self, host: str, system_prompt: str = None, model: str = None):
        self.client = Client(host=host)
        self.model = model
        self.system_prompt = system_prompt

    def chat(self, user_prompt: str):
        messages = ([{'role': 'system', 'content': self.system_prompt}] if self.system_prompt else []) + \
           [{'role': 'user', 'content': user_prompt}]

        return self.client.chat(model=self.model, messages=messages, stream=False)
