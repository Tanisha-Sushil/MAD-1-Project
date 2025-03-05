from main import app
from flask import render_template, redirect, url_for, request, flash, session
from application.models import *
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

@app.route("/")
def index():
    if session.get('name', None):
        professions = Profession.query.all()
        return render_template('index.html', professions=professions)
    return render_template('index.html')

@app.route('/add_profession', methods=['GET', 'POST'])
def add_profession():
    if request.method == 'GET':
        return render_template('add_profession.html')
    
    if request.method == 'POST':
        name = request.form.get('profession_name')

        if not name:
            flash('Profession name is required')
            return redirect(url_for('add_profession'))
        
        ex_profession = Profession.query.filter_by(name=name).first()

        if ex_profession:
            flash("Profession Name already exist", 'danger')
            return redirect(url_for('add_profession'))
        
        if session['role'] == 'admin':
            try:
                new_profession = Profession(name=name)
                db.session.add(new_profession)
                db.session.commit()
                flash('Profession name added successfully', 'success')
                return redirect(url_for('add_profession'))
            except Exception as e:
                flash(f'Error adding Profession name!! Error: {e}', 'danger')
                return redirect(url_for('add_profession'))
            
@app.route('/add_services', methods=['GET', 'POST'])
def add_services():
    if request.method == 'GET':
        professions = Profession.query.all()
        return render_template('add_services.html', professions=professions)
    
    if request.method == 'POST':
        service_name = request.form.get('service_name')
        description = request.form.get('description')
        charges = int(request.form.get('charges'))
        service_time = int(request.form.get('service_time'))
        profession_id = request.form.get('profession')

    #Data Validation
    if not service_name or not description or not charges or not service_time:
        flash("All fields are required", 'danger')
        return redirect(url_for('add_services'))
    
    profession = Profession.query.filter_by(id=profession_id).first()
    if not profession:
        flash("Invalid profession", 'danger')
        return redirect(url_for('add_services'))
    
    if session['role'] == 'admin':
        new_service = Service(name=service_name,
                              description=description,
                              charges=charges,
                              service_time=service_time,
                              profession_id=profession.id)
        try:
            db.session.add(new_service)
            db.session.commit()
            flash("New Service added successfully", 'success')
            return redirect(url_for('add_services'))
        except Exception as e:
            flash(f'Error in adding service! Error: {e}', 'danger')
            return redirect(url_for('add_services'))
        
@app.route('/edit_services/<int:id>', methods=['GET', 'POST'])
def edit_services(id):
    service = Service.query.filter_by(id=id).first()

    if not service:
        flash('Service not found', 'danger')
        return redirect(url_for('index'))
    
    profession = Profession.query.all()
    if request.method == 'GET':
        return render_template('edit_services.html', profession=profession, service=service)
    
    if request.method == 'POST':
        service_name = request.form.get('service_name')
        description = request.form.get('description')
        charges = int(request.form.get('charges'))
        service_time = int(request.form.get('service_time'))
        profession_id = request.form.get('profession')

        #Data Validation
        service = Service.query.filter_by(id=id).first()
        if service_name:
            service.name=service_name
        if description:
            service.description=description
        if charges:
            service.charges=charges
        if service_time:
            service.service_time=service_time
        if profession_id:
            profession = Profession.query.filter_by(id=profession_id).first()
            if not profession:
                flash('Invalid Profession', 'danger')
                return redirect(url_for('edit_services', profession=profession))
            service.profession_id=profession.id

        try:
            db.session.commit()
            flash('Service updated Successfully', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error updating service! Erorr: {e}', 'danger')
            return redirect(url_for('edit_sevices', id=id))

@app.route('/delete_service/<int:id>', methods=['GET', 'POST'])
def delete_service(id):
    service = Service.query.filter_by(id=id).first()

    if not service:
        flash('Service not found', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('delete_services.html', service=service)
    
    if request.method == 'POST':
        if session['role'] == 'admin':
            try:
                db.session.delete(service)
                db.session.commit()
                flash('Service deleted successsfully', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f'Error deleting service! Error: {e}', 'danger')
                return redirect(url_for('delete_service', service=service))
        else:
            flash('Unauthorized Access', 'danger')
            return redirect(url_for('index'))




##########

@app.route('/block_user/<int:id>', methods=['GET'])
def block_user(id):
    if session.get('role', None) == 'admin':
        user = User.query.filter_by(id=id).first()
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('view_users'))
        user.is_blocked = True
        db.session.commit()
        flash('User Blocked Successfully', 'success')
        return redirect(url_for('view_users'))
    else:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('index'))
    
@app.route('/unblock_user/<int:id>', methods=['GET'])
def unblock_user(id):
    if session.get('role', None) == 'admin':
        user = User.query.filter_by(id=id).first()
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('view_users'))
        user.is_blocked = False
        db.session.commit()
        flash('User Unblocked Successfully', 'success')
        return redirect(url_for('view_users'))
    else:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('index'))

@app.route('/reject_professional/<int:id>', methods=['GET'])
def reject_professional(id):
    if session.get('role', None) == 'admin':
        user = User.query.filter_by(id=id).first()
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('view_users')) 
        professional = Professional.query.filter_by(user_id=user.id).first()
        if professional:
            db.session.delete(professional)
        db.session.delete(user)
        db.session.commit()
        flash('Professional signup request rejected', 'danger')
        return redirect(url_for('view_users'))
    else:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('index'))

@app.route('/approve_professional/<int:id>', methods=['GET'])
def approve_professional(id):
    if session.get('role', None) == 'admin':
        user = User.query.filter_by(id=id).first()
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('view_users'))
        professional = Professional.query.filter_by(user_id=user.id).first()

        if not professional and user.roles[0].role == 'professional':
            db.session.delete(user)
            db.session.commit()
            flash('Professional signup request rejected', 'danger')
            return redirect(url_for('view_users'))
        
        professional.is_approved = True
        db.session.commit()
        flash('Professional Approved Successfully', 'success')
        return redirect(url_for('view_users'))
    else:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('index'))

@app.route('/view_users', methods=['GET'])
def view_users():
    if session.get('role', None) == 'admin':
        users = User.query.all()
        approved_professionals = []
        unapproved_professionals = []
        customer = []
        for user in users:
            if user.roles[0].role == 'customer':
                customer.append(user)
            elif user.roles[0].role == 'admin':
                continue
            else:
                professional_details = Professional.query.filter_by(user_id = user.id).first()
                if not professional_details:
                    unapproved_professionals.append(user)
                    continue
                user.document_url = professional_details.document_url
                user.experience = professional_details.experience
                user.is_approved = professional_details.is_approved
                user.profession = Profession.query.filter_by(id=professional_details.profession_id).first().name
                if user.is_approved:
                    approved_professionals.append(user)
                else:
                    unapproved_professionals.append(user)
        return render_template('users.html', approved_professionals=approved_professionals, unapproved_professionals=unapproved_professionals,customers = customer)
    else:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('index'))
    
@app.route('/view_service/<int:id>', methods=['GET'])
def view_service(id):
    service = Service.query.filter_by(id=id).first()
    if not service:
        flash('Service not found', 'danger')
        return redirect(url_for('index'))
    professionals = Professional.query.filter_by(profession_id=service.profession_id, is_approved = True).all()
    users = []
    for professional in professionals:
        user = User.query.filter_by(id=professional.user_id).first()
        user.experience = professional.experience
        user.document_url = professional.document_url
        user.profession = Profession.query.filter_by(id=professional.profession_id).first().name
        users.append(user)
    return render_template('book_professionals.html', service=service, users = users)


@app.route('/book_professional/<int:professional_id>/<int:service_id>', methods=['GET'])
def book_professional(professional_id, service_id):
    user = User.query.filter_by(email=session['email']).first()
    
    professional = User.query.filter_by(id=professional_id).first()
    if not professional:
        flash('Professional not found', 'danger')
        return redirect(url_for('index'))
    if professional.roles[0].role != 'professional':
        flash('Invalid Professional', 'danger')
        return redirect(url_for('index'))
     
    if Professional.query.filter_by(user_id=professional.id).first().is_approved == False:
        flash('Professional not approved', 'danger')
        return redirect(url_for('index'))

    service_request = ServiceRequest(user_id=user.id, 
                   professional_id=professional_id, 
                   service_id=service_id, 
                   service_date=datetime.now(),
                   status='pending')
    db.session.add(service_request)
    db.session.commit()
    flash('Service Requested Successfully', 'success')
    return redirect(url_for('index'))


@app.route('/view_requests', methods=['GET'])
def view_requests():
    user = User.query.filter_by(email=session['email']).first()
    if user.roles[0].role == 'customer':
        service_requests = ServiceRequest.query.filter_by(user_id=user.id).all()
        requests = []
        for request in service_requests:
            professional = User.query.filter_by(id=request.professional_id).first()
            professional_details = Professional.query.filter_by(user_id=professional.id).first()
            professional.profession = Profession.query.filter_by(id=professional_details.profession_id).first().name
            service = Service.query.filter_by(id=request.service_id).first()
            request.professional = professional
            request.service = service
            request.professional_experience = professional_details.experience
            requests.append(request)
        return render_template('view_requests.html', service_requests=requests)
        
    if user.roles[0].role == 'professional':
        service_requests = ServiceRequest.query.filter_by(professional_id=user.id).all()
        requests = []
        for request in service_requests:
            customer = User.query.filter_by(id=request.user_id).first()
            service = Service.query.filter_by(id=request.service_id).first()
            request.customer = customer
            request.service = service
            requests.append(request)
        return render_template('view_requests.html', service_requests=requests)

@app.route('/accept_request/<int:id>', methods=['GET'])
def accept_request(id):
    service_request = ServiceRequest.query.filter_by(id=id).first()
    if not service_request:
        flash('Request not found', 'danger')
        return redirect(url_for('view_requests'))
    
    if not service_request.professional_id == User.query.filter_by(email=session['email']).first().id:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('view_requests'))
    
    service_request.status = 'accepted'
    db.session.commit()
    flash('Request Approved Successfully', 'success')
    return redirect(url_for('view_requests'))

@app.route('/reject_request/<int:id>', methods=['GET'])
def reject_request(id):
    service_request = ServiceRequest.query.filter_by(id=id).first()
    if not service_request:
        flash('Request not found', 'danger')
        return redirect(url_for('view_requests'))
    
    if not service_request.professional_id == User.query.filter_by(email=session['email']).first().id:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('view_requests'))
    
    service_request.status = 'rejected'
    db.session.commit()
    flash('Request Rejected Successfully', 'success')
    return redirect(url_for('view_requests'))

@app.route('/complete_request/<int:id>', methods=['GET'])
def complete_request(id):
    service_request = ServiceRequest.query.filter_by(id=id).first()
    if not service_request:
        flash('Request not found', 'danger')
        return redirect(url_for('view_requests'))
    
    if not service_request.professional_id == User.query.filter_by(email=session['email']).first().id:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('view_requests'))
    
    service_request.status = 'completed'
    db.session.commit()
    flash('Request Completed Successfully', 'success')
    return redirect(url_for('view_requests'))

@app.route('/rate_request/<int:id>', methods=['POST'])
def rate_request(id):
    service_request = ServiceRequest.query.filter_by(id=id).first()
    if not service_request:
        flash('Request not found', 'danger')
        return redirect(url_for('view_requests'))
        
    rating = request.form.get('rating')
    review = request.form.get('review')
    if not rating:
        flash('Rating is required', 'danger')
        return redirect(url_for('view_requests'))
    
    service_request.rating = 2 * int(rating)
    service_request.review = review
    db.session.commit()
    flash('Request Rated Successfully', 'success')
    return redirect(url_for('view_requests'))



@app.route('/search', methods=['POST'])
def search():
    search = request.form.get('search')
    if not search:
        flash('Search field is required', 'danger')
        return redirect(url_for('index'))
      
    services = Service.query.filter(Service.name.like(f'%{search}%')).all()
    
    professions = Profession.query.filter(Profession.name.like(f'%{search}%')).all()
    for profession in professions:
        profession.services = Service.query.filter_by(profession_id=profession.id).all()       
    
    return render_template('search.html', services=services, professions=professions)


@app.route('/summary', methods=['GET'])
def summary():
    if session.get('role', None) == 'admin':
        users = User.query.all()
        total_customers = 0
        total_professionals = 0
        for user in users:
            if user.roles[0].role == 'customer':
                total_customers += 1
            if user.roles[0].role == 'professional':
                total_professionals += 1

        total_services = Service.query.count()
        total_requests = ServiceRequest.query.count()

        #professional wise total earnings
        professionals = Professional.query.all()
        earnings = {}
        for professional in professionals:
            user = User.query.filter_by(id=professional.user_id).first()
            earnings[user.name] = 0
            requests = ServiceRequest.query.filter_by(professional_id=professional.user_id, status='completed').all()
            for request in requests:
                service = Service.query.filter_by(id=request.service_id).first()
                earnings[user.name] += service.charges
        # plot graph for earnings using matplotlib
        total_earnings = sum(earnings.values())
        plt.figure(figsize=(10, 5))
        plt.bar(earnings.keys(), earnings.values())
        plt.xlabel('Professionals')
        plt.ylabel('Earnings')
        plt.title('Professional Earnings')
        #save file in agg mode and send the url to template
        plt.savefig('static/earnings.png')
        plt.close()
        return render_template('summary.html', 
                               total_customers=total_customers,
                               total_professionals=total_professionals,
                             total_services=total_services, 
                             total_earnings=total_earnings, 
                             earnings_graph='static/earnings.png')


    else:
        flash('Unauthorized Access', 'danger')
        return redirect(url_for('index'))
        
    