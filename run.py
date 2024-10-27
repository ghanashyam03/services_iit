from Code.create_app import create_app
from Code.extensions import db

app = create_app()

with app.app_context():
    db.create_all()  # Create tables based on current model definitions
    print("Database tables have been created.")

if __name__ == '__main__':
    app.run(debug=True)