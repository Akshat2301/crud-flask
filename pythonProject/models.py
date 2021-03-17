from flask_login import UserMixin

from pythonProject import db,login_manager


@login_manager.user_loader
def load_user(user_id):
    return emp_details.query.get(int(user_id))


class emp_details(db.Model, UserMixin):
    """
    id,name,email,phone_num,msg,date
    """

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String, primary_key=False)
    lastName = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(12), nullable=True)
    password = db.Column(db.String(21), nullable=False)