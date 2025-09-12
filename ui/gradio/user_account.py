import gradio as gr
import json
from db.db_table_management import create_user, get_user_by_username, get_all_users
from db.constants import DB_PATH


def Usubmit_form(
        username
):
    u = create_user(username)
    print(u)
    g = get_all_users()
    print(g)

with gr.Blocks() as demo:
    gr.Markdown("## User")

    with gr.Row():
        username = gr.Textbox(label="Write you username", placeholder="Username")
    submit_button = gr.Button(value="Submit")
    output = gr.Textbox(label="Done")
    submit_button.click(fn=Usubmit_form, inputs=[username], outputs=output)

if __name__ == "__main__":
    demo.launch()