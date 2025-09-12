import gradio as gr

import ui.gradio.main_page as main_page
import ui.gradio.admin as admin
import ui.gradio.knowledge_profile as knowledge_profile
import ui.gradio.learning_profile as learning_profile
import ui.gradio.user_account as user_account
from db.db_management import init_db

with gr.Blocks() as demo:
    main_page.demo.render()
with demo.route("Admin"):
    admin.demo.render()
with demo.route("Knowledge Profil"):
    knowledge_profile.demo.render()
with demo.route("Learning Profil"):
    learning_profile.demo.render()
with demo.route("User"):
    user_account.demo.render()

if __name__ == "__main__":
    init_db()
    demo.launch()
