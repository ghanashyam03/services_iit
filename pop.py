from Code.create_app import create_app
from Code.extensions import db
from Code.models import Admin, ServiceProfessional, Customer, Service, ServiceRequest

# Create the Flask app
app = create_app()



# Predefined services
predefined_services = [
  
    {'name': 'Cleaning', 'price': 30.0, 'time_required': '3 hours', 'description': 'General house cleaning services'},
    {'name': 'Electrical', 'price': 60.0, 'time_required': '1 hour', 'description': 'Electrical repairs and installations'},
    {'name': 'Painting', 'price': 100.0, 'time_required': '5 hours', 'description': 'House painting services'},
    {'name': 'Carpentry', 'price': 70.0, 'time_required': '4 hours', 'description': 'Woodwork and carpentry services'},
    {'name': 'Gardening', 'price': 40.0, 'time_required': '2 hours', 'description': 'Gardening and landscaping services'}
]

with app.app_context():
    db.create_all()  # Ensure all tables are created
    db.session.query(Service).delete()
    db.session.commit()
   
    print("Services have been added to the database.")