import sqlite3 as sql
from profiles.knowledge_profile import KnowledgeProfile
from profiles.learner_profile import LearnerProfile
from db.constants import DB_PATH


def create_admin(username: str):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("INSERT INTO admins (admin_username) VALUES (?)", (username,))

    conn.commit()
    conn.close()


def create_user(username: str):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("INSERT INTO users (username) VALUES (?)", (username,))

    conn.commit()
    conn.close()


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
                    user_id, name, age, background, familiarity_kw, math_eq, programming_comfort, confidence_asking, support_needs
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
        user_id,
        knowledge_profile.name,
        knowledge_profile.age,
        knowledge_profile.background,
        knowledge_profile.familiarity_kw,
        knowledge_profile.math_eq,
        knowledge_profile.programming_comfort,
        knowledge_profile.confidence_asking,
        ", ".join(knowledge_profile.support_needs)
    ))

    conn.commit()
    conn.close()


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
        name=row[2],
        age=row[3],
        background=row[4],
        familiarity_kw=row[5],
        math_eq=row[6],
        programming_comfort=row[7],
        confidence_asking=row[8],
        support_needs=row[9]
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
                    user_id, problematic, goal_understanding, precision_level, analogies, conciseness, 
                    learning_mode, explanation_style, interactivity, tone, humor, motivation, adaptability
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
        user_id,
        learner_profile.problematic,
        learner_profile.goal_understanding,
        learner_profile.precision_level,
        learner_profile.analogies,
        learner_profile.conciseness,
        learner_profile.learning_mode,
        learner_profile.explanation_style,
        learner_profile.interactivity,
        learner_profile.tone,
        learner_profile.humor,
        learner_profile.motivation,
        learner_profile.adaptability
    ))

    conn.commit()
    conn.close()


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
        problematic=row[2],
        goal_understanding=row[3],
        precision_level=row[4],
        analogies=row[5],
        conciseness=row[6],
        learning_mode=row[7],
        explanation_style=row[8],
        interactivity=row[9],
        tone=row[10],
        humor=row[11],
        motivation=row[12],
        adaptability=row[13]
    )

    return learner_profile


# def set_kp_value_by_username(username, field, value):
#     conn = sql.connect(DB_PATH)
#     cur = conn.cursor()
#
#     user_id = get_user_id_by_username(username)
#     if user_id is None:
#         raise ValueError(f"User '{username}' does not exist.")
#
#     if field not in {"background", "familiarity_kw", "math_eq", "programming_comfort", "confidence_asking", "support_needs"}:
#         raise ValueError(f"Invalid field '{field}' for KnowledgeProfile.")
#
#     query = f"UPDATE knowledge_profiles SET {field} = ? WHERE user_id = ?"
#     cur.execute(query, (value, user_id))
#
#     conn.commit()
#     conn.close()
#
#
# def set_lp_value_by_username(username, field, value):
#     conn = sql.connect(DB_PATH)
#     cur = conn.cursor()
#
#     user_id = get_user_id_by_username(username)
#     if user_id is None:
#         raise ValueError(f"User '{username}' does not exist.")
#
#     if field not in {"goal_understanding", "problematic", "explanation_style", "precision_level", "analogies",
#                      "conciseness", "interactivity", "tone", "humor", "motivation", "learning_mode", "adaptability"}:
#         raise ValueError(f"Invalid field '{field}' for LearnerProfile.")
#
#     query = f"UPDATE learner_profiles SET {field} = ? WHERE user_id = ?"
#     cur.execute(query, (value, user_id))
#
#     conn.commit()
#     conn.close()


def get_all_users():
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    conn.close()

    return rows


def get_all_knowledge_profiles():
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM knowledge_profiles")
    rows = cur.fetchall()

    conn.close()

    return rows


def get_all_learner_profiles():
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM learner_profiles")
    rows = cur.fetchall()

    conn.close()

    return rows


def get_user_by_username(username):
    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    conn.close()

    return row
