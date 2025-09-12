import gradio as gr

with gr.Blocks() as demo:
    # Header
    with gr.Row():
        gr.Markdown("<h1 style='text-align:center'>Welcome to Mind MeSH</h1>")

    # Instructions section
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("""
            <h2 style="color:blue; font-size:36px; text-align:center; font-style:italic;">
            How to Use The Agent
            </h2>

            <ol>
                <li>Step 1</li>
                <li>Step 2</li>
                <li>Step 3</li>
                <li>Step 4</li>
            </ol>

            <p style="color:red; font-weight:bold;">⚠️ Warning Message if needed</p>
            """)

if __name__ == "__main__":
    demo.launch()
