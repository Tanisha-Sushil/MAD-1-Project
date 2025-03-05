from flask import Flask, render_template, url_for, request
from application.database import db
from application.config import Config
from application.models import *

def create_app():
    app = Flask(__name__, template_folder='template')

    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

        admin_role=Role.query.filter_by(role='admin').first()
        if not admin_role:
            admin_role = Role(role='admin')
            db.session.add(admin_role)

        professional=Role.query.filter_by(role='professional').first()
        if not professional:
            professional = Role(role='professional')
            db.session.add(professional)

        customer=Role.query.filter_by(role='customer').first()
        if not customer:
            customer = Role(role='customer')
            db.session.add(customer)

        admin=User.query.filter_by(name='Admin').first()
        print(admin)
        if not admin:
            admin = User(name='Admin',
                         gender='Male',
                         contact_no=9848339388,
                         address='Mumbai',
                         pincode='400012',
                         email='admin@gmail.com',
                         password='admin',
                         pfp_url='pfp',
                         is_blocked=False,
                         roles=[admin_role])
            db.session.add(admin)

        db.session.commit()

    return app

app = create_app()

from application.routes import *
from application.auth_routes import *

if __name__ == "__main__":
    app.run(debug = True, port=8000)
