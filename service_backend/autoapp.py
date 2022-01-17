"""Create an application instance."""
from backend import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
