# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 14:04:18 2025

@author: maxyo
"""

import sqlite3, json
from .questionnaire import LearnerProfile, asdict


# --- DB
def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS learner_profiles (
        learner_id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_json TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def save_profile(profile: LearnerProfile, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    profile_json = json.dumps(asdict(profile))
    cur.execute("INSERT INTO learner_profiles (profile_json) VALUES (?)", (profile_json,))
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