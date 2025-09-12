# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 19:51:50 2025

@author: maxyo
"""

import gradio as gr
from db.db_management import LPsubmit_form


# -------------------------
# Gradio UI
# -------------------------
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Learning Profile Questionnaire")
    
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
    output = gr.Textbox(label="Result")

    submit_btn.click(
        fn=LPsubmit_form,
        inputs=[goal_understanding, problematic, explanation_style, precision_level, 
                analogies, conciseness, interactivity, tone, humor, motivation, learning_mode, adaptability], 
                outputs=output
        )

demo.launch()