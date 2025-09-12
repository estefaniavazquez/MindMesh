import gradio as gr
import sqlite3
import db.db_management as db_management
from db.db_table_management import create_user

with gr.Blocks() as demo:
    gr.Markdown("## User")

    with gr.Row():
        username = gr.Textbox(label="Write you username", placeholder="Username")
    submit_button = gr.Button(value="Submit")
    output = gr.Textbox(label="Done")
    submit_button.click(fn=create_user, inputs=[username], outputs=output)

if __name__ == "__main__":
    db_management.init_db()
    demo.launch()