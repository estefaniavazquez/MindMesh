import gradio as gr
from llm.agent import Agent

system_prompt = """system prompt"""

def inference(prompt, hf_token, model, model_name):
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    if hf_token is None or not hf_token.trip():
        hf_token = os.getenv("HF_TOKEN")
    Client = InferenceClient(model=model, token-hf_token)
    tokens = f"**'{model_name}'**\n\n"
    for completion in client.chat.completion(messages, max_tokens=100, stream=True):
        token = completion.choices[0].delta.content
        tokens += token
        yeild tokens

with gr.Blocks() as demo:
    gr.Markdown("<center><h1>MindMeSH Agent<h1></center>")
    username = gr.Textbox(label="Username", placeholder="Enter your username")
    prompt = gr.Textbox(label="Prompt", placeholder="Enter your message", lines=3)
    token = gr.Textbox(label="Token", placeholder="Enter your token")

    with gr.Row():
        generate_btn = gr.Button("Generate")

    with gr.Row() as output:
        agent_output = gr.Markdown("Agent Output")


    gr.on(
        triggers=[prompt.submit, generate_btn.click],
        fn=inference,
        inputs=[prompt, token],
        outputs=[agent_output],
        show_progress="hidden"
    )



demo.launch()