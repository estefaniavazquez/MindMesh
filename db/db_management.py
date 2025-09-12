# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 14:04:18 2025

@author: maxyo
"""

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
            print("Database connection closed")


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
            print("Database connection closed")


def init_db():
    print("Initializing database at: ", DB_PATH)

    conn = sql.connect(DB_PATH)
    print("Database connection established")

    cur = conn.cursor()

    print("Creating tables")

    print("Creating Admin table")
    initialize_admins_table(cur)

    print("Creating User table")
    initialize_users_table(cur)

    print("Creating Knowledge Profiles table")
    initialize_knowledge_profiles_table(cur)

    print("Creating Learner Profiles table")
    initialize_learner_profiles_table(cur)

    print("Tables created successfully")

    conn.commit()
    print("Commit successful")

    conn.close()
    print("Database connection closed")


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
            goal_understanding INTEGER NOT NULL,
            problematic TEXT NOT NULL,
            explanation_style TEXT NOT NULL,
            precision_level INTEGER NOT NULL,
            analogies INTEGER NOT NULL,
            conciseness INTEGER NOT NULL,
            interactivity TEXT NOT NULL,
            tone TEXT NOT NULL,
            humor TEXT NOT NULL,
            motivation TEXT NOT NULL,
            learning_mode INTEGER NOT NULL,
            adaptability TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
    """)
