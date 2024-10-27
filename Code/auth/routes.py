from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from Code.extensions import db
from Code.models import Admin, ServiceProfessional, Customer

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        if user_type == 'admin':
            user = Admin.query.filter_by(email=email).first()
        elif user_type == 'professional':
            user = ServiceProfessional.query.filter_by(email=email).first()
        else:
            user = Customer.query.filter_by(email=email).first()
        

        if user and check_password_hash(user.password, password):
            if user_type == 'professional' and not user.is_approved:
                flash('Your account is waiting for approval.', 'warning')
                return render_template('login.html')
            session['user_id'] = user.id
            session['user_type'] = user_type
            if user_type == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user_type == 'professional':
                return redirect(url_for('professional_actions.dashboard'))
            else:
                return redirect(url_for('service_requests.view_requests'))
        else:
            flash('Invalid email or password.', 'danger')
        
    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        hashed_password = generate_password_hash(password, method='sha256')
        
        if user_type == 'professional':
            service_type = request.form.get('service_type')
            experience = request.form.get('experience')
            new_user = ServiceProfessional(name=name, email=email, password=hashed_password, service_type=service_type, experience=experience)
        else:
            new_user = Customer(name=name, email=email, password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')