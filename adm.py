from Code.create_app import create_app
from Code.extensions import db
from Code.models import Admin
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.drop_all()  # Drop all existing tables
    db.create_all()  # Recreate tables based on current model definitions

    admin = Admin(username='admin', email='admin@example.com', password=generate_password_hash('adminpassword', method='sha256'))
    db.session.add(admin)
    db.session.commit()
    print("Admin user has been added to the database.")