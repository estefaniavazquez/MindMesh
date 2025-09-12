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


def get_user_id_by_username(username: str):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]  # Return user_id

    return None


def create_knowledge_profile(username, knowledge_profile: KnowledgeProfile):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    user_id = get_user_id_by_username(username)
    if user_id is None:
        raise ValueError(f"User '{username}' does not exist.")

    cur.execute("""
                INSERT INTO knowledge_profiles (
                    user_id, background, familiarity_kw, math_eq, programming_comfort, confidence_asking, support_needs
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
        user_id,
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


def get_knowledge_profile_by_username(username):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    user_id = get_user_id_by_username(username)

    cur.execute("SELECT * FROM knowledge_profiles WHERE user_id = ?", (user_id,))
    row = cur.fetchone()

    conn.close()

    if row is None:
        raise ValueError(f"User '{username}' does not exist.")

    knowledge_profile = KnowledgeProfile(
        name=row[0],
        age=row[1],
        background=row[2],
        familiarity_kw=row[3],
        math_eq=row[4],
        programming_comfort=row[5],
        confidence_asking=row[6],
        support_needs=row[7]
    )

    return knowledge_profile


def create_learner_profile(username, learner_profile: LearnerProfile):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    user_id = get_user_id_by_username(username)
    if user_id is None:
        raise ValueError(f"User '{username}' does not exist.")

    cur.execute("""
                INSERT INTO learner_profiles (
                    user_id, goal_understanding, problematic, explanation_style, precision_level, analogies,
                    conciseness, interactivity, tone, humor, motivation, learning_mode, adaptability
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
        user_id,
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


def get_learner_profile_by_username(username):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    user_id = get_user_id_by_username(username)

    cur.execute("SELECT * FROM learner_profiles WHERE user_id = ?", (user_id,))
    row = cur.fetchone()

    conn.close()

    if row is None:
        raise ValueError(f"User '{username}' does not exist.")

    learner_profile = LearnerProfile(
        goal_understanding=row[0],
        problematic=row[1],
        explanation_style=row[2],
        precision_level=row[3],
        analogies=row[4],
        conciseness=row[5],
        interactivity=row[6],
        tone=row[7],
        humor=row[8],
        motivation=row[9],
        learning_mode=row[10],
        adaptability=row[11]
    )

    return learner_profile


def set_kp_value_by_username(username, field, value):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    user_id = get_user_id_by_username(username)
    if user_id is None:
        raise ValueError(f"User '{username}' does not exist.")

    if field not in {"background", "familiarity_kw", "math_eq", "programming_comfort", "confidence_asking", "support_needs"}:
        raise ValueError(f"Invalid field '{field}' for KnowledgeProfile.")

    query = f"UPDATE knowledge_profiles SET {field} = ? WHERE user_id = ?"
    cur.execute(query, (value, user_id))

    conn.commit()
    conn.close()


def set_lp_value_by_username(username, field, value):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    user_id = get_user_id_by_username(username)
    if user_id is None:
        raise ValueError(f"User '{username}' does not exist.")

    if field not in {"goal_understanding", "problematic", "explanation_style", "precision_level", "analogies",
                     "conciseness", "interactivity", "tone", "humor", "motivation", "learning_mode", "adaptability"}:
        raise ValueError(f"Invalid field '{field}' for LearnerProfile.")

    query = f"UPDATE learner_profiles SET {field} = ? WHERE user_id = ?"
    cur.execute(query, (value, user_id))

    conn.commit()
    conn.close()


def get_all_users():
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    conn.close()

    return [(rid, username) for rid, username in rows]


def get_all_knowledge_profiles():
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM knowledge_profiles")
    rows = cur.fetchall()

    conn.close()

    return [(rid, json.loads(js)) for rid, js in rows]


def get_all_learner_profiles():
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM learner_profiles")
    rows = cur.fetchall()

    conn.close()

    return [(rid, json.loads(js)) for rid, js in rows]


def get_user_by_username(username):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    conn.close()

    if row:
        return row[0], row[1]  # Return (user_id, username)

    return None
