import os
from huggingface_hub import InferenceClient
from db.db_table_management import get_knowledge_profile_by_username, get_learner_profile_by_username


class Agent:
    def __init__(self, username, model="openai/gpt-oss-120b"):
        self.username = username
        self.knowledge_profile = get_knowledge_profile_by_username(username)
        self.learning_profile = get_learner_profile_by_username(username)
        self.history = []
        self.client = InferenceClient(
            provider="cerebras",
            api_key=os.environ.get("HF_TOKEN")
        )
        self.model = model


    def system_prompt(self):
        context_prompt = f"""
        You are an AI assistant for a user named {self.username}.
        They have the following knowledge profile: {self.knowledge_profile}
        They have the following learning profile: {self.learning_profile}
        Use this information to tailor your responses.
        """
        self.history.append({"role": "system", "content": context_prompt})


    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            max_tokens=512
        )

        assistant_output = response.choices[0].message['content']
        self.history.append({"role": "assistant", "content": assistant_output})

        return assistant_output


    def reset(self):
        self.history = []
        self.system_prompt()
