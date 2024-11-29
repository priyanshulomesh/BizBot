import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db  # Absolute import to access create_app and db

app = create_app()
with app.app_context():
    # Drop all tables
    db.drop_all()
    # Create new tables
    db.create_all()
