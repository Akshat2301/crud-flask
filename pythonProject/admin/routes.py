from flask import Blueprint
from flask import render_template, request, session, redirect, flash, url_for
from pythonProject.models import emp_details
from pythonProject import db, params
from pythonProject.user.forms import RegistrationForm

admin = Blueprint('admin', __name__)


@admin.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    form = RegistrationForm()
    if 'user' in session and session['user'] == params['admin_user']:
        page = request.args.get('page', 1, type=int)
        emps = emp_details.query.paginate(page=page, per_page=params['ROWS_PER_PAGE'], error_out=False)
        return render_template('index.html', params=params, emps=emps,form=form)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if username == params['admin_user'] and userpass == params['admin_password']:
            # set the session variable
            session['user'] = username
            return redirect(url_for('admin.dashboard'))

        else:
            flash("Enter correct credentials")
            return render_template('admin_login.html', params=params)

    else:
        return render_template('admin_login.html', params=params)


@admin.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    form = RegistrationForm()
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        page = request.args.get('page', 1, type=int)
        emps = emp_details.query.filter(emp_details.firstName.like(search)).paginate(page=page,
                                                                                     per_page=params['ROWS_PER_PAGE'],
                                                                                     error_out=False)
        return render_template('index.html', params=params, emps=emps, form=form)
    else:
        page = request.args.get('page', 1, type=int)
        emps = emp_details.query.paginate(page=page, per_page=params['ROWS_PER_PAGE'],
                                          error_out=False)
        return render_template('index.html', params=params, emps=emps, form=form)


@admin.route("/add_employee", methods=['GET', 'POST'])
def add_employee():
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
        return redirect(url_for('admin.dashboard'))

    emps = emp_details.query.all()
    return render_template('index.html', params=params, emps=emps, form=form)


@admin.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        post = emp_details.query.filter_by(id=sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('admin.admin_login'))


@admin.route("/logout")
def logout():
    session.pop('user')
    session.clear()
    return redirect(url_for('admin.admin_login'))