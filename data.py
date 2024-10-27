from Code.create_app import create_app
from Code.extensions import db
from Code.models import Admin, ServiceProfessional, Customer, Service, ServiceRequest

app = create_app()

with app.app_context():
    # Query and print data from Admin table
    admins = Admin.query.all()
    print("Admins:")
    for admin in admins:
        print(f"ID: {admin.id}, Username: {admin.username}, Email: {admin.email}")

    # Query and print data from ServiceProfessional table
    professionals = ServiceProfessional.query.all()
    print("\nService Professionals:")
    for professional in professionals:
        print(f"ID: {professional.id}, Name: {professional.name}, Email: {professional.email}, Service Type: {professional.service_type}, Experience: {professional.experience}, Approved: {professional.is_approved}")

    # Query and print data from Customer table
    customers = Customer.query.all()
    print("\nCustomers:")
    for customer in customers:
        print(f"ID: {customer.id}, Name: {customer.name}, Email: {customer.email}")

    # Query and print data from Service table
    services = Service.query.all()
    print("\nServices:")
    for service in services:
        print(f"ID: {service.id}, Name: {service.name}, Price: {service.price}, Time Required: {service.time_required}, Description: {service.description}")

    # Query and print data from ServiceRequest table
    service_requests = ServiceRequest.query.all()
    print("\nService Requests:")
    for request in service_requests:
        print(f"ID: {request.id}, Service ID: {request.service_id}, Customer ID: {request.customer_id}, Professional ID: {request.professional_id}, Date of Request: {request.date_of_request}, Date of Completion: {request.date_of_completion}, Status: {request.service_status}, Remarks: {request.remarks}")