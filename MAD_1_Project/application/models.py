from application.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    contact_no = db.Column(db.Integer, unique=True)
    address = db.Column(db.String(255))
    pincode = db.Column(db.Integer)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    pfp_url = db.Column(db.String(100))
    is_blocked = db.Column(db.Boolean, default=False)

    #Relationship
    roles = db.relationship('Role', secondary='user_role', backref=db.backref('user', lazy='select'))

    def __repr__(self):
        return f'<User (self.name)>'

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Role (self.role)>'

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class Profession(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)


    services = db.relationship('Service', backref='profession', lazy=True)

    def __repr__(self):
        return f'<Profession {self.name}>'

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profession_id = db.Column(db.Integer, db.ForeignKey('profession.id'))
    experience = db.Column(db.Integer, nullable=False)
    document_url = db.Column(db.String(100), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    charges = db.Column(db.Integer, nullable=False)
    service_time = db.Column(db.Integer, nullable=False)
    profession_id = db.Column(db.Integer, db.ForeignKey('profession.id'), nullable=False)

    def __repr__(self):
        return f'<Service {self.name}>'

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    service_date = db.Column(db.Date, nullable=False)
    # charges = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(255), nullable=True)


