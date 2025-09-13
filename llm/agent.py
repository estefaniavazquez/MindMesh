import os
from huggingface_hub import InferenceClient
from db.db_table_management import get_knowledge_profile_by_username, get_learner_profile_by_username
from dotenv import load_dotenv


class Agent:
    def __init__(self, username, model="openai/gpt-oss-120b"):
        load_dotenv()

        self.username = username
        self.knowledge_profile = get_knowledge_profile_by_username(username)
        self.learning_profile = get_learner_profile_by_username(username)
        self.chat_history = []
        self.client = InferenceClient(
            provider="cerebras",
            api_key=os.environ.get("HF_TOKEN")
        )
        self.model = model


    def build_knowledge_profile_description(self):
        if not self.knowledge_profile:
            return "No knowledge profile available."

        description = (
            f"Name: {self.knowledge_profile.name}\n"
            f"Age: {self.knowledge_profile.age}\n"
            f"Background and for how long: {self.knowledge_profile.background}\n"
            f"Proficiency with scientific background: {self.knowledge_profile.familiarity_kw}\n"
            f"Comfort with Equations/Mathematics: {self.knowledge_profile.math_eq}\n"
            f"Comfort with Programming/Tools: {self.knowledge_profile.programming_comfort}\n"
            f"Confidence in Asking Questions: {self.knowledge_profile.confidence_asking}\n"
            f"Support Needs: {', '.join(self.knowledge_profile.support_needs)}"
        )

        return description


    def build_learning_profile_description(self):
        if not self.learning_profile:
            return "No learning profile available."

        description = (
            f"The main goals and challenges of the project are: {self.learning_profile.problematic}\n"
            f"Current level of understanding on the project's goal and problems: {self.learning_profile.goal_understanding}\n"
            f"Preference for technical precision (1) vs simplified explanations (10): {self.learning_profile.precision_level}\n"
            f"Enjoyment of learning through stories and analogies (1-10): {self.learning_profile.analogies}\n"
            f"Preference for short concise summaries (1) vs long detailed explanations (10): {self.learning_profile.conciseness}\n"
            f"Preference for learning by trial-and-error with feedback (1) vs structured guidance (10): {self.learning_profile.learning_mode}\n"
            f"Preferred explanation style: {self.learning_profile.explanation_style}\n"
            f"Desire for the AI to quiz your understanding: {self.learning_profile.interactivity}\n"
            f"Preferred communication style (tone): {self.learning_profile.tone}\n"
            f"Preferred interaction style (humour): {self.learning_profile.humor}\n"
            f"Desire for motivational phrases: {self.learning_profile.motivation}\n"
            f"Desire for the AI to adapt its style over time as it learns from them: {self.learning_profile.adaptability}"
        )

        return description


    def system_prompt(self):
        context_prompt = f"""
        You are an AI assistant for a user named {self.username}.
        \n\nThey have the following knowledge profile: {self.build_knowledge_profile_description()}
        \n\nThey have the following learning profile: {self.build_learning_profile_description()}
        \n\nUse this information to tailor your responses.
        """
        self.chat_history.append({"role": "system", "content": context_prompt})


    def send_message(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.chat_history,
            max_tokens=512
        )

        assistant_output = response.choices[0].message['content']
        self.chat_history.append({"role": "assistant", "content": assistant_output})

        return assistant_output


    def delete_chat_history(self):
        self.chat_history = []
        self.system_prompt()
