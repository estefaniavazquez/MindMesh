import os

root_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(root_dir, "database.db")
print("Database path: ", DB_PATH)