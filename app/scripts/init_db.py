# USAGE:
# From the project root, run either:
#   python -m app.scripts.init_db
# or
#   PYTHONPATH=. python app/scripts/init_db.py
# This ensures the 'app' module is found.

from app.storage.db import init_db

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized.")
