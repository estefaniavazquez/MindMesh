import gradio as gr
from db.db_management import KPsubmit_form

# -------------------------
# Gradio UI
# -------------------------
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Knowledge Profile Questionnaire")

    with gr.Row():
        name = gr.Textbox(label="What is your name?")
        age = gr.Textbox(label="How old are you?")
    
    background = gr.Textbox(label="What is your academic background and for how long?")
    
    familiarity_kw = gr.Textbox(label="What are you proficient in with your scientific background?")

    math_eq = gr.Slider(0, 10, step=1, label="How comfortable are you with reading equations or mathematical expressions? (0–10)")
    
    programming_comfort = gr.Slider(0, 10, step=1, label="How comfortable are you with programming or computational tools? (0–10)")

    confidence_asking = gr.Slider(0, 10, step=1, label="How confident are you in asking questions when you don’t understand something? (0–10)")

    support_needs = gr.CheckboxGroup(
        ["Project problematic", "Mathemathics", "Statistics", "Programming", "Biological Sciences", 
         "Biomedical Sciences", "Chemistry", "Physics", "Astronomy", "Environmental Sciences", 
         "Computer Sciences", "Engineering", "Medical Sciences", ], label="Support Needs"
    )

    submit_btn = gr.Button("Submit Profile")
    output = gr.Textbox(label="Result")

    submit_btn.click(
        fn=KPsubmit_form,
        inputs=[name, age, background, familiarity_kw, math_eq, programming_comfort, confidence_asking, support_needs],
        outputs=output
    )

demo.launch()
