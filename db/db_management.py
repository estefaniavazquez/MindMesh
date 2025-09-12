import sqlite3 as sql
from sqlite3 import Cursor
from db.constants import DB_PATH


def clear_db_data():
    try:
        conn = sql.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("DELETE FROM admins")
        cur.execute("DELETE FROM users")
        cur.execute("DELETE FROM knowledge_profiles")
        cur.execute("DELETE FROM learner_profiles")

        conn.commit()

        print("Database data cleared")

    except sql.Error as e:
        print("Error clearing database's data: ", e)

    finally:
        if conn:
            conn.close()


def clear_db():
    try:
        conn = sql.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS admins")
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS knowledge_profiles")
        cur.execute("DROP TABLE IF EXISTS learner_profiles")

        conn.commit()

        print("Database cleared")

    except sql.Error as e:
        print("Error clearing database: ", e)

    finally:
        if conn:
            conn.close()


def init_db():
    print("Initializing database at: ", DB_PATH)

    conn = sql.connect(DB_PATH)
    cur = conn.cursor()

    print("Creating tables")
    initialize_admins_table(cur)
    initialize_users_table(cur)
    initialize_knowledge_profiles_table(cur)
    initialize_learner_profiles_table(cur)
    print("Tables created successfully")

    conn.commit()
    conn.close()


def initialize_admins_table(cur: Cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_username TEXT NOT NULL UNIQUE
        )
    """)


def initialize_users_table(cur: Cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        )
    """)


def initialize_knowledge_profiles_table(cur: Cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_profiles (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            background TEXT NOT NULL,
            familiarity_kw TEXT NOT NULL,
            math_eq INTEGER NOT NULL,
            programming_comfort INTEGER NOT NULL,
            confidence_asking INTEGER NOT NULL,
            support_needs TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
    """)


def initialize_learner_profiles_table(cur: Cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS learner_profiles (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            problematic TEXT NOT NULL,
            goal_understanding INTEGER NOT NULL,
            precision_level INTEGER NOT NULL,
            analogies INTEGER NOT NULL,
            conciseness INTEGER NOT NULL,
            learning_mode INTEGER NOT NULL,
            explanation_style TEXT NOT NULL,
            interactivity INTEGER NOT NULL,
            tone TEXT NOT NULL,
            humor TEXT NOT NULL,
            motivation TEXT NOT NULL,
            adaptability TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
    """)
