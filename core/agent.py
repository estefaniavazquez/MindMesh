import os
from huggingface_hub import InferenceClient

class Agent:
    def __init__(self, username, model="openai/gpt-oss-120b"):
        self.username = username
        self.knowledge_profile = None
        self.learning_profile = None
        self.history = []
        self.client = InferenceClient(
            provider="cerebras",
            api_key=os.environ.get("HF_TOKEN")
        )
        self.model = model

        self.system_prompt()

    def fetch_knowledge_profile(self):
        # TODO: Implement fetching knowledge profile from database

        self.knowledge_profile = "Has a CS background."

    def fetch_learning_profile(self):
        # TODO: Implement fetching learning profile from database

        self.learning_profile = "Prefers step-by-step reasoning with examples."


    def system_prompt(self):
        self.fetch_knowledge_profile()
        self.fetch_learning_profile()

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


estefania_agent = Agent(
    username="Estefania"
)

# Chat
print(estefania_agent.chat("Can you explain what an LLM is?"))
print(estefania_agent.chat("Now, give me a real-world analogy."))