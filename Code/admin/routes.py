from flask import Blueprint, render_template, redirect, url_for, request, session
from Code.extensions import db
from Code.models import Admin, ServiceProfessional, Customer, Service

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
def dashboard():
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    return render_template('admin_dashboard.html')

@admin.route('/manage_users')
def manage_users():
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    professionals = ServiceProfessional.query.all()
    customers = Customer.query.all()
    return render_template('manage_users.html', professionals=professionals, customers=customers)

@admin.route('/manage_services')
def manage_services():
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    services = Service.query.all()
    return render_template('manage_services.html', services=services)

@admin.route('/approve_professional/<int:id>')
def approve_professional(id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    professional = ServiceProfessional.query.get(id)
    professional.is_approved = True
    db.session.commit()
    return redirect(url_for('admin.manage_users'))

@admin.route('/block_user/<user_type>/<int:id>')
def block_user(user_type, id):
    if session.get('user_type') != 'admin':
        return redirect(url_for('auth.login'))
    if user_type == 'professional':
        user = ServiceProfessional.query.get(id)
    else:
        user = Customer.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.manage_users'))

@admin.route('/')
def home():
    return render_template('home.html')
