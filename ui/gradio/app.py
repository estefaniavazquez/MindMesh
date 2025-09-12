import gradio as gr

import ui.gradio.main_page as main_page
import ui.gradio.admin as admin
import ui.gradio.knowledge_profile as knowledge_profile
import ui.gradio.learning_profile as learning_profile
import ui.gradio.user_account as user_account
from db.db_management import init_db, clear_db_data, clear_db
from db.db_table_management import get_learner_profile_by_username, get_knowledge_profile_by_username

with gr.Blocks() as demo:
    main_page.demo.render()
with demo.route("Admin"):
    admin.demo.render()
with demo.route("Knowledge Profile"):
    knowledge_profile.demo.render()
with demo.route("Learning Profile"):
    learning_profile.demo.render()
with demo.route("User"):
    user_account.demo.render()

if __name__ == "__main__":
    # clear_db_data()
    # clear_db()
    init_db()
    ckp = get_knowledge_profile_by_username("Ramzi")
    print(ckp)
    clp = get_learner_profile_by_username("Ramzi")
    print(clp)
    demo.launch()
