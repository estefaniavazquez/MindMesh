import gradio as gr
from llm.agent import Agent

agent = None

def create_agent(username):
    global agent
    agent = Agent(username)
    agent.system_prompt()
    return gr.update(visible=True)

def agent_chat(message, history):
    response = agent.send_message(message)
    return response

with gr.Blocks() as demo:
    gr.Markdown("## MindMeSH Chat Agent")

    username_textbox = gr.Textbox(label="Enter your username", placeholder="Username")
    start_button = gr.Button("Start Chat")

    with gr.Group(visible=False) as chat_ui_group:
        chat_ui = gr.ChatInterface(
            fn=agent_chat,
            title="Chat",
            type="messages",
            save_history=True,
        )

    start_button.click(
        fn=create_agent,
        inputs=[username_textbox],
        outputs=[chat_ui_group]
    )

if __name__ == "__main__":
    demo.launch()
