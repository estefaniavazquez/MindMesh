# import pytest
# import sqlite3 as sql
# import os
#
# from db.db_table_management import (
#     create_admin, create_user, create_knowledge_profile, create_learner_profile, get_user_id_by_username
# )
# from db.db_management import init_db
# from db.constants import DB_PATH
# from profiles.knowledge_profile import KnowledgeProfile
# from profiles.learner_profile import LearnerProfile
#
#
# def setup_module():
#     if os.path.exists(DB_PATH):
#         os.remove(DB_PATH)
#
#     init_db()
#
#
# def teardown_module():
#     if os.path.exists(DB_PATH):
#         os.remove(DB_PATH)
#
#
# def admin_creation():
#     print("Testing admin creation...")
#
#     create_admin("estefania")
#
#     create_admin("maxyo")
#
#     with pytest.raises(sql.IntegrityError):
#         create_admin("estefania")
#
#
# def user_creation():
#     print("Testing user creation...")
#
#     create_user("estefania")
#
#     create_user("maxyo")
#
#     with pytest.raises(sql.IntegrityError):
#         create_user("estefania")
#
#
# def knowledge_profile_and_learner_profile_attach_to_user():
#     print("Testing attaching profiles to user...")
#
#     username = "estefania"
#
#     kp = KnowledgeProfile(
#         name="Estefania Vazquez", age="24", background="Software Engineering", familiarity_kw="Calculus",
#         math_eq=7, programming_comfort=7, confidence_asking=7, support_needs=["Examples", "Step-by-step explanations"]
#     )
#     create_knowledge_profile(username, kp)
#
#     with pytest.raises(sql.IntegrityError):
#         create_knowledge_profile(username, kp)
#
#     lp = LearnerProfile(
#         goal_understanding=5, problematic="None", explanation_style="Simple",
#         precision_level=2, analogies=1, conciseness=3, interactivity="High",
#         tone="Friendly", humor="Yes", motivation="Strong", learning_mode=1, adaptability="High"
#     )
#     create_learner_profile(username, lp)
#
#     with pytest.raises(sql.IntegrityError):
#         create_learner_profile(username, lp)
