from flask import Blueprint, render_template, redirect, url_for, request, session
from Code.extensions import db
from Code.models import Service, ServiceRequest

service_management = Blueprint('service_management', __name__)

@service_management.route('/create_service', methods=['GET', 'POST'])
def create_service():
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        time_required = request.form.get('time_required')
        description = request.form.get('description')
        new_service = Service(name=name, price=price, time_required=time_required, description=description)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('admin.manage_services'))
    return render_template('create_service.html')

@service_management.route('/update_service/<int:id>', methods=['GET', 'POST'])
def update_service(id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    service = Service.query.get(id)
    if request.method == 'POST':
        service.name = request.form.get('name')
        service.price = request.form.get('price')
        service.time_required = request.form.get('time_required')
        service.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('admin.manage_services'))
    return render_template('update_service.html', service=service)

@service_management.route('/delete_service/<int:id>')
def delete_service(id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    
    service = Service.query.get(id)
    
    # Delete all related service requests before deleting the service
    ServiceRequest.query.filter_by(service_id=id).delete()
    
    db.session.delete(service)
    db.session.commit()
    
    return redirect(url_for('admin.manage_services'))
