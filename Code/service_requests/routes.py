from flask import Blueprint, render_template, redirect, url_for, request, session
from Code.extensions import db
from Code.models import ServiceRequest, Service, Customer
from datetime import datetime

service_requests = Blueprint('service_requests', __name__)

@service_requests.route('/create_request', methods=['GET', 'POST'])
def create_request():
    if session.get('user_type') != 'customer':
        return redirect(url_for('auth.login'))
    
    predefined_services = Service.query.all()  # Fetch services from the database
    print(predefined_services)
    for service in predefined_services:
        print(service.name)

    if request.method == 'POST':
        service_id = request.form.get('service_id')
        customer_id = session.get('user_id')
        date_of_request_str = request.form.get('date_of_request')
        date_of_request = datetime.strptime(date_of_request_str, '%Y-%m-%d')
        new_request = ServiceRequest(service_id=service_id, customer_id=customer_id, date_of_request=date_of_request)
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('service_requests.view_requests'))
    
    return render_template('create_request.html', services=predefined_services)

@service_requests.route('/edit_request/<int:id>', methods=['GET', 'POST'])
def edit_request(id):
    if session.get('user_type') != 'customer':
        return redirect(url_for('auth.login'))
    service_request = ServiceRequest.query.get(id)
    if request.method == 'POST':
        service_id = request.form.get('service_id')
        if service_id:
            service_request.service_id = service_id
        date_of_request_str = request.form.get('date_of_request')
        service_request.date_of_request = datetime.strptime(date_of_request_str, '%Y-%m-%d')
        service_request.remarks = request.form.get('remarks')
        db.session.commit()
        return redirect(url_for('service_requests.view_requests'))
    predefined_services = Service.query.all()
    return render_template('edit_request.html', service_request=service_request, services=predefined_services)

@service_requests.route('/close_request/<int:id>')
def close_request(id):
    if session.get('user_type') != 'customer':
        return redirect(url_for('auth.login'))
    service_request = ServiceRequest.query.get(id)
    db.session.delete(service_request)
    db.session.commit()
    return redirect(url_for('service_requests.view_requests'))

@service_requests.route('/view_requests')
def view_requests():
    if session.get('user_type') != 'customer':
        return redirect(url_for('auth.login'))
    
    customer_id = session.get('user_id')
    requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    
    return render_template('view_requests.html', requests=requests)