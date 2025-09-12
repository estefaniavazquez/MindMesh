import gradio as gr
from db.db_table_management import create_user, get_user_by_username, get_all_users


def Usubmit_form(
        username
):
    create_user(username)

    print(get_all_users())


with gr.Blocks() as demo:
    gr.Markdown("## User")

    with gr.Row():
        username = gr.Textbox(label="Write you username", placeholder="Username")

    submit_button = gr.Button(value="Submit")

    submit_button.click(
        fn=Usubmit_form,
        inputs=[username]
    )


if __name__ == "__main__":
    demo.launch()
