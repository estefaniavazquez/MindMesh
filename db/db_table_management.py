import sqlite3 as sql
import json

from profiles.knowledge_profile import KnowledgeProfile
from profiles.learner_profile import LearnerProfile
from db.constants import DB_PATH


def create_admin(username: str):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("INSERT INTO admins (admin_username) VALUES (?)", (username,))

    conn.commit()
    conn.close()

    return cur.lastrowid


def create_user(username: str):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("INSERT INTO users (username) VALUES (?)", (username,))

    conn.commit()
    conn.close()

    return cur.lastrowid


def create_knowledge_profile(knowledge_profile: KnowledgeProfile):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                INSERT INTO knowledge_profiles (
                    background, familiarity_kw, math_eq, programming_comfort, confidence_asking, support_needs
                ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
        knowledge_profile.background,
        knowledge_profile.familiarity_kw,
        knowledge_profile.math_eq,
        knowledge_profile.programming_comfort,
        knowledge_profile.confidence_asking,
        ", ".join(knowledge_profile.support_needs)
    ))

    conn.commit()
    conn.close()

    return cur.lastrowid


def create_learner_profile(learner_profile: LearnerProfile):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                INSERT INTO learner_profiles (
                    goal_understanding, problematic, explanation_style, precision_level, analogies,
                    conciseness, interactivity, tone, humor, motivation, learning_mode, adaptability
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
        learner_profile.goal_understanding,
        learner_profile.problematic,
        learner_profile.explanation_style,
        learner_profile.precision_level,
        learner_profile.analogies,
        learner_profile.conciseness,
        learner_profile.interactivity,
        learner_profile.tone,
        learner_profile.humor,
        learner_profile.motivation,
        learner_profile.learning_mode,
        learner_profile.adaptability
    ))

    conn.commit()
    conn.close()

    return cur.lastrowid


def get_all_users(db_path):
    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    conn.close()

    return [(rid, username) for rid, username in rows]


def get_all_knowledge_profiles(db_path):
    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM knowledge_profiles")
    rows = cur.fetchall()

    conn.close()

    return [(rid, json.loads(js)) for rid, js in rows]


def get_all_learner_profiles(db_path):
    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM learner_profiles")
    rows = cur.fetchall()

    conn.close()

    return [(rid, json.loads(js)) for rid, js in rows]


def get_user_by_username(db_path, username):
    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    conn.close()

    if row:
        return row[0], row[1]  # Return (user_id, username)

    return None


def get_knowledge_profile_by_username(db_path, username):
    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
                SELECT kp.* FROM knowledge_profiles kp
                JOIN users u ON kp.knowledge_profile_id = u.user_id
                WHERE u.username = ?
                """, (username,))
    row = cur.fetchone()

    conn.close()

    if row:
        return row[0], json.loads(row[1])  # Return (knowledge_profile_id, profile_data)

    return None


def get_learner_profile_by_username(db_path, username):
    conn = sql.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
                SELECT lp.* FROM learner_profiles lp
                JOIN users u ON lp.learner_profile_id = u.user_id
                WHERE u.username = ?
                """, (username,))
    row = cur.fetchone()

    conn.close()

    if row:
        return row[0], json.loads(row[1])  # Return (learner_profile_id, profile_data)

    return None