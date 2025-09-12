import gradio as gr
import os
from llm.agent import Agent
from dotenv import load_dotenv   # ✅ pour charger le .env

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Dictionary to store agents by username (chaque utilisateur garde son historique)
agents = {}

def inference(username, prompt, token=None):
    if not username or not username.strip():
        return "⚠️ Please enter a username."

    # Si on a fourni un token en UI, on met à jour HF_TOKEN
    if token and token.strip():
        os.environ["HF_TOKEN"] = token

    # Créer un Agent si pas déjà existant
    if username not in agents:
        agents[username] = Agent(username=username)
        agents[username].system_prompt()

    agent = agents[username]

    # Envoyer le message utilisateur et récupérer la réponse
    response = agent.send_message(prompt)
    return response


with gr.Blocks() as demo:
    gr.Markdown("<center><h1>MindMeSH Agent</h1></center>")

    username = gr.Textbox(label="Username", placeholder="Enter your username")
    prompt = gr.Textbox(label="Prompt", placeholder="Enter your message", lines=3)
    token = gr.Textbox(label="Token", placeholder="Enter your HF token (optional)", type="password")

    with gr.Row():
        generate_btn = gr.Button("Generate")

    with gr.Row() as output:
        agent_output = gr.Markdown("Agent Output")

    gr.on(
        triggers=[prompt.submit, generate_btn.click],
        fn=inference,
        inputs=[username, prompt, token],
        outputs=[agent_output],
        show_progress="hidden"
    )

demo.launch()
