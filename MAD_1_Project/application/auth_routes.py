from main import app
from flask import render_template, request, redirect, url_for, flash, session
from application.models import User, Role, Profession, Professional
from application.models import db

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('All fields required', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Invalid Email", 'danger')
            return redirect(url_for('login'))
        
        if user.password != password:
            flash("Invalid Password", 'danger')
            return redirect(url_for('login'))
        
        if user.roles[0].role == 'professional':
            Professional_details = Professional.query.filter_by(user_id = user.id).first()
            if Professional_details.is_approved == False:
                flash("Your account is not approved by admin")
                return redirect(url_for('login'))
            
        if user.is_blocked == True:
                flash("Account blocked by admin")
                return redirect(url_for('login'))

        session['name'] = user.name
        session['email'] = user.email
        session['role'] = user.roles[0].role
        
        flash("Login Successful", 'Success')
        return redirect(url_for('index'))
    
@app.route("/logout")
def logout():
    session.pop('name', None)
    session.pop('email', None)
    session.pop('role', None)
    flash("Logged out successfull", 'success')
    return redirect(url_for('index'))

@app.route("/register", methods=['GET', 'Post'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        contact_no = request.form.get('contact_no')
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')
        pincode = request.form.get('pincode')
        role = request.form.get('role')
        pfp = request.files.get('pfp')

        #Data validation
        if not name or not gender or not contact_no or not email or not password or not address or not pincode or not role:
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))
        
        if len(password)<5:
            flash('Password must contain 5 characters', 'danger')
            return redirect(url_for('register'))
        
        if '@' not in email or '.' not in email:
            flash('Invalid Email', 'danger')
            return redirect(url_for('register'))
        
        if len(contact_no)!=10:
            flash('Invalid Contact Number', 'danger')
            return redirect(url_for('register'))
        
        if len(pincode)!=6:
            flash('Invalid Pincode', 'danger')
            return redirect(url_for('register'))
        
        try:
            role = Role.query.filter_by(role=role).first()
            if not role:
                flash("Invalid Role", 'danger')
                return redirect(url_for('register'))
            user = User.query.filter_by(email=email).first()
            if user:
                flash("Email already exist", 'danger')
                return redirect(url_for('register'))
            user = User.query.filter_by(contact_no=contact_no).first()
            if user:
                flash("Contact Number already exist", 'danger')
                return redirect(url_for('register'))
            image_file_path = None
            if pfp:
                image_file_path = 'images/' + pfp.filename
                absoulte_path = 'static/' + image_file_path
                pfp.save(absoulte_path)
            user = User(name=name, email=email, password=password, address=address, roles=[role], gender=gender, contact_no=contact_no, pincode=pincode, pfp_url=image_file_path)
            db.session.add(user)
            db.session.commit()
            #### 
            if role.role == 'professional':
                flash('Professional Registered Successfully. Complete your profile and await for admin approval')
                return redirect(url_for('prof_register',id = user.id))

            else:
                flash('User Registered Successfully', 'Success')
                return redirect(url_for('login'))
            ####
            # flash('User Registered Successfully', 'Success')
            # return redirect(url_for('login'))
        except Exception as e:
            flash(f"User Registration Failed. {e}", 'danger')
            return redirect(url_for('register'))
        
@app.route('/prof_register/<int:id>', methods = ['GET','POST'])
def prof_register(id):
    if request.method == 'GET':
        professions = Profession.query.all()
        return render_template('prof_register.html',user_id = id,professions=professions)
    
    if request.method == "POST":
        profesion_id = request.form.get('profession',None)
        id_proof = request.files.get("id_proof", None)
        experience = request.form.get("experience", None)

        if not experience:
            flash("Experence can't be empty")
            return render_template('prof_register.html',user_id = id,professions=professions)
        
        if not id_proof:
            flash("Upload ID Proof")
            return render_template('prof_register.html',user_id = id,professions=professions)
        
        if not profesion_id:
            flash("Select the Profession")
            return render_template('prof_register.html',user_id = id,professions=professions)
        
        try: 
            if id_proof:
                document_path = 'documents/'+id_proof.filename
                relative_path = 'static/' + document_path
                id_proof.save(relative_path)
            
            profesional = Professional(user_id = id,
                                    profession_id=profesion_id,
                                    experience=experience,
                                    document_url = document_path,
                                    is_approved = False,
                                    )
            
            db.session.add(profesional)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            flash("Oopss Something went wrong")
            return redirect(url_for(prof_register,id=id))



        