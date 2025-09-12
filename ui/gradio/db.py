# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 14:04:18 2025

@author: maxyo
"""

import sqlite3, json
from dataclasses import dataclass, asdict, field
from typing import List


# --- Profil
DB_PATH = "Projet IC.db"

# -------------------------
#  
# -------------------------
def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS learner_profiles (
        learner_id INTEGER PRIMARY KEY AUTOINCREMENT,
        knowledge_profile TEXT NOT NULL,
        learning_profile TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_profile(knowledge_profile, learning_profile, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    knowledge_json = json.dumps(asdict(knowledge_profile))
    learning_json = json.dumps(asdict(learning_profile)) if learning_profile else None
    cur.execute("""
        INSERT INTO learner_profiles (knowledge_profile, learning_profile)
        VALUES (?, ?)
    """, (knowledge_json, learning_json))
    conn.commit()
    learner_id = cur.lastrowid
    conn.close()
    return learner_id

def load_profiles(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT learner_id, profile_json FROM learner_profiles")
    rows = cur.fetchall()
    conn.close()
    return [(rid, json.loads(js)) for rid, js in rows]



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
    goal_understanding: int = 0
    problematic: str = ""
    explanation_style: str = ""
    precision_level: int = 0
    analogies: int = 0
    conciseness: int = 0
    interactivity: str = ""
    tone: str = ""
    humor: str = ""
    motivation: str = ""
    learning_mode: int = 0
    adaptability: str = ""
    
    
    
# -------------------------
# LearnerProfile Gradio logic
# -------------------------
def LPsubmit_form(goal_understanding, problematic, explanation_style, precision_level, 
                  analogies, conciseness, interactivity, tone, humor, motivation, 
                  learning_mode, adaptability):

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