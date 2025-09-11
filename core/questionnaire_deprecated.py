# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 14:02:32 2025

@author: maxyo
"""

from dataclasses import dataclass, asdict, field
from typing import List
from .db import save_profile

# --- Profil
DB_PATH = "Projet IC.db"



# -------------------------
# KnowledgeProfile dataclass
# -------------------------
@dataclass
class KnowledgeProfile:
    name: str = ""
    age: str = ""
    background: str = ""
    familiarity_kw: str = ""
    math_eq: int = 0
    programming_comfort: int = 0
    confidence_asking: int = 0
    support_needs: List[str] = field(default_factory=list)
    
    
    
# -------------------------
# KnowledgeProfile Gradio logic
# -------------------------
def KPsubmit_form(name, age, background, familiarity_kw, math_eq, programming_comfort, confidence_asking, support_needs):

    kp = KnowledgeProfile(
        name=name,
        age=age,
        background=background,
        familiarity_kw=familiarity_kw,
        math_eq=math_eq,
        programming_comfort=programming_comfort,
        confidence_asking=confidence_asking,
        support_needs=support_needs
    )

    learner_id = save_profile(kp, None, DB_PATH)
    return f"✅ Profile saved with ID {learner_id}"

    

# -------------------------
# LearnerProfile dataclass
# -------------------------
@dataclass
class LearnerProfile:
    goal_understanding: float
    problematic: str
    explanation_style: int
    precision_level: float
    analogies: float
    conciseness: float
    interactivity: int
    tone: float
    humor: float
    motivation: int
    learning_mode: int
    adaptability: int
    
    
    
# -------------------------
# LearnerProfile Gradio logic
# -------------------------
def LPsubmit_form(goal_understanding, problematic, explanation_style, precision_level, 
                  analogies, conciseness, interactivity, tone, humor, motivation, 
                  learning_mode, adaptability
                  ):

    lp = LearnerProfile(
        goal_understanding=goal_understanding,
        problematic=problematic,
        explanation_style=explanation_style,
        precision_level=precision_level,
        analogies=analogies,
        conciseness=conciseness,
        interactivity=interactivity,
        tone=tone,
        humor=humor,
        motivation=motivation,
        learning_mode=learning_mode,
        adaptability=adaptability
    )

    learner_id = save_profile(None, lp, DB_PATH)
    return f"✅ Profile saved with ID {learner_id}"