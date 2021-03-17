from flask import Blueprint
from flask import render_template, request, session, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user
from pythonProject.models import emp_details
from pythonProject import params, db
from pythonProject.user.forms import RegistrationForm, LoginForm


users = Blueprint('users', __name__)


@users.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        emp = emp_details.query.filter_by(id=current_user.id).first()
        other_emp = emp_details.query.all()
        return render_template('profile.html', emp=emp, other_emp=other_emp)
    if form.validate_on_submit():
        user = emp_details.query.filter_by(email=form.emailID.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            emp = emp_details.query.filter_by(email=user.email).first()
            return redirect(url_for('users.profile', sno=emp.id))
        else:
            flash('Invalid username or Password', 'warning')
    return render_template('login.html', form=form)


@users.route("/logout_emp")
def logout_emp():
    logout_user()
    return redirect('/')


@users.route("/edit/<string:sno>/<string:flag>", methods=['GET', 'POST'])
def edit(sno, flag):
    emp = emp_details.query.filter_by(id=sno).first()
    if current_user.is_authenticated or ('user' in session and session['user'] == params['admin_user']):
        if request.method == 'POST':
            fname = request.form.get('firstName')
            lname = request.form.get('lastName')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address = request.form.get('address')
            dob = request.form.get('DOB')
            password = request.form.get('password')
            cpassword = request.form.get('cpassword')
            emp = emp_details.query.filter_by(id=sno).first()
            if emp.email == email or (emp_details.query.filter_by(email=email).first() is None):
                emp.firstName = fname
                emp.lastName = lname
                emp.email = email
                emp.phone = phone
                emp.address = address
                emp.dob = dob
                emp.password = password
                db.session.commit()
                # return redirect('user./edit/' + sno + '/' + flag)
                return redirect(url_for('users.edit', sno=emp.id, flag=flag))
            else:
                flash('This email id is already registered', 'danger')
        emp = emp_details.query.filter_by(id=sno).first()
        return render_template('edit.html', params=params, emp=emp, id=sno, flag=flag)
    else:
        return redirect(url_for('users.login'))


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        '''Add Entry to the Database'''
        fname = form.firstName.data
        lname = form.lastName.data
        email = form.email.data
        phone = form.phone.data
        dob = form.dob.data
        address = form.address.data
        password = form.password.data

        entry = emp_details(firstName=fname, lastName=lname, phone=phone, address=address, email=email, dob=dob,
                            password=password)
        db.session.add(entry)
        db.session.commit()
        # flash('Successfully Registered', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form, params=params)


@users.route("/profile/<string:sno>")
def profile(sno):
    if current_user.is_authenticated:
        emp = emp_details.query.filter_by(id=sno).first()
        other_emp = emp_details.query.all()
        return render_template('profile.html', params=params, emp=emp, other_emp=other_emp)
    else:
        return redirect(url_for('users.login'))
