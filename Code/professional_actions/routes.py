from flask import Blueprint, render_template, redirect, url_for, request, session
from Code.extensions import db
from Code.models import ServiceRequest, ServiceProfessional, RejectedRequest
from datetime import datetime

professional_actions = Blueprint('professional_actions', __name__)

@professional_actions.route('/dashboard')
def dashboard():
    if session.get('user_type') != 'professional':
        return redirect(url_for('auth.login'))
    
    professional_id = session.get('user_id')
    professional = ServiceProfessional.query.get(professional_id)
    
    # Fetch requests that match the professional's service type and are either requested or under process by the same professional
    requests = ServiceRequest.query.filter(
        (ServiceRequest.service_id == professional.service_type) &
        ((ServiceRequest.service_status == 'requested') | 
         ((ServiceRequest.service_status == 'under process') & (ServiceRequest.professional_id == professional_id))) &
        ~ServiceRequest.rejected_requests.any(RejectedRequest.professional_id == professional_id)
    ).all()
    
    return render_template('professional_dashboard.html', requests=requests)

@professional_actions.route('/view_requests')
def view_requests():
    if session.get('user_type') != 'professional':
        return redirect(url_for('auth.login'))
    professional_id = session.get('user_id')
    requests = ServiceRequest.query.filter_by(professional_id=professional_id).all()
    return render_template('view_requests.html', requests=requests)

@professional_actions.route('/accept_request/<int:id>')
def accept_request(id):
    if session.get('user_type') != 'professional':
        return redirect(url_for('auth.login'))
    
    professional_id = session.get('user_id')
    service_request = ServiceRequest.query.get(id)
    
    # Ensure the request is still in the 'requested' status before accepting
    if service_request.service_status == 'requested':
        service_request.service_status = 'under process'
        service_request.professional_id = professional_id
        db.session.commit()
    
    return redirect(url_for('professional_actions.dashboard'))

@professional_actions.route('/reject_request/<int:id>')
def reject_request(id):
    if session.get('user_type') != 'professional':
        return redirect(url_for('auth.login'))
    
    professional_id = session.get('user_id')
    service_request = ServiceRequest.query.get(id)
    
    # Add an entry to the RejectedRequest table
    rejected_request = RejectedRequest(service_request_id=service_request.id, professional_id=professional_id)
    db.session.add(rejected_request)
    db.session.commit()
    
    return redirect(url_for('professional_actions.dashboard'))

@professional_actions.route('/finish_request/<int:id>')
def finish_request(id):
    if session.get('user_type') != 'professional':
        return redirect(url_for('auth.login'))
    service_request = ServiceRequest.query.get(id)
    service_request.service_status = 'finished'
    service_request.date_of_completion = datetime.now()
    db.session.commit()
    return redirect(url_for('professional_actions.dashboard'))