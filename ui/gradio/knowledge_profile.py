import gradio as gr
from db.db_table_management import create_knowledge_profile
from profiles.knowledge_profile import KnowledgeProfile

def KPsubmit_form(
        name, age, background, familiarity, math_eq, programming_comfort, confidence_asking, support_needs
):
    kp = KnowledgeProfile(
        name=name,
        age=age,
        background=background,
        familiarity_kw=familiarity,
        math_eq=math_eq,
        programming_comfort=programming_comfort,
        confidence_asking=confidence_asking,
        support_needs=support_needs,
    )
    create_knowledge_profile(kp)
# -----------------------------
# Build Gradio interface
# -----------------------------

with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Knowledge Profile Questionnaire")

    with gr.Row():
        name = gr.Textbox(label="What is your name?")
        age = gr.Textbox(label="How old are you?")

    background = gr.Textbox(label="What is your academic background and for how long?")
    familiarity_kw = gr.Textbox(label="What are you proficient in with your scientific background?")

    math_eq = gr.Slider(0, 10, step=1, label="Comfort with equations/mathematics (0–10)")
    programming_comfort = gr.Slider(0, 10, step=1, label="Comfort with programming/tools (0–10)")
    confidence_asking = gr.Slider(0, 10, step=1, label="Confidence in asking questions (0–10)")

    support_needs = gr.CheckboxGroup(
        ["Project problematic", "Mathematics", "Statistics", "Programming", "Biological Sciences", 
         "Biomedical Sciences", "Chemistry", "Physics", "Astronomy", "Environmental Sciences", 
         "Computer Sciences", "Engineering", "Medical Sciences"],
        label="Support Needs"
    )

    submit_btn = gr.Button("Submit Profile")
    output = gr.Textbox(label="Result", interactive=False)

    # Connect submit button to database function
    submit_btn.click(
        fn=KPsubmit_form,
        inputs=[name, age, background, familiarity_kw,
                math_eq, programming_comfort, confidence_asking,
                support_needs],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()
