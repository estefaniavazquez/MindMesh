import gradio as gr
from profiles.learner_profile import LearnerProfile
from db.db_table_management import create_learner_profile, get_all_learner_profiles, get_learner_profile_by_username


def LPsubmit_form(
    username, problematic, goal_understanding, precision_level, analogies, conciseness, learning_mode, explanation_style, interactivity, tone, humor, motivation, adaptability
):
    lp = LearnerProfile(
        problematic=problematic,
        goal_understanding=goal_understanding,
        precision_level=precision_level,
        analogies=analogies,
        conciseness=conciseness,
        learning_mode=learning_mode,
        explanation_style=explanation_style,
        interactivity=interactivity,
        tone=tone,
        humor=humor,
        motivation=motivation,
        adaptability=adaptability
    )
    create_learner_profile(username, lp)

    print(get_all_learner_profiles())


with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Learning Profile Questionnaire")

    username = gr.Textbox(label="Username")
    
    problematic = gr.Textbox(label="Please describe, in your own words, what you think the main goals and challenges are.")
    
    goal_understanding = gr.Slider(0, 10, step=1, label="What do you feel is your current level of understanding of this project’s overarching goal and problems? (0–10)")

    precision_level = gr.Slider(0, 10, step=1, label="Do you prefer technical precision or simplified explanations?")

    analogies = gr.Slider(0, 10, step=1, label="Do you enjoy learning through stories and analogies?")

    conciseness = gr.Slider(0, 10, step=1, label="Do you prefer short concise summaries or long detailed explanations?")

    learning_mode = gr.Slider(0, 10, step=1, label="Do you prefer to learn by trial-and-error with feedback or structured guidance?")

    explanation_style = gr.Radio(["Step-by-step", "Analogy-driven", "Big-picture-first", "Details-first"], label="How do you prefer new concepts to be explained? ")

    interactivity = gr.Radio(["No", "Yes"], label="Do you want the AI to quiz you back to check understanding?")

    tone = gr.Radio(["Formal", "Casual"], label="Do you prefer a formal or casual communication style?")

    humor = gr.Radio(["Playful/Humorous", "Serious/Focused"], label="Do you prefer the AI to be more playful/humorous or serious/focused?")

    motivation = gr.Radio(["No", "Yes"], label="Do you want the AI to encourage you with motivational phrases?")

    adaptability = gr.Radio(["No", "Yes"],  label="Should the AI adapt its style over time as it learns from you? ")

    submit_btn = gr.Button("Submit Profile")

    submit_btn.click(
        fn=LPsubmit_form,
        inputs=[username, problematic, goal_understanding, precision_level, analogies, conciseness, learning_mode,
                explanation_style, interactivity, tone, humor, motivation, adaptability],
        )


if __name__ == "__main__":
    demo.launch()
