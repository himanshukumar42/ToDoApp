from flask import Blueprint, request, render_template, redirect
from flask import flash, session, url_for
from flask_session import Session

from application import db
from werkzeug.security import generate_password_hash, check_password_hash

from app.user.models import User
from app.tasks.models import Task
from app.utility.form import LoginForm, RegisterForm
import app.utility.validate as validate
import os

print("+++++++++++++ Current Working Directory")
print(os.getcwd())
user_endpoints = Blueprint('user_endpoints', __name__, static_folder="app/user/static", template_folder='templates/')


@user_endpoints.errorhandler(500)
def error_500_server(e):
    return render_template('500.html'), 500


@user_endpoints.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@user_endpoints.route('/login', methods=['GET', 'POST'])
def login():
    print("++++++++++ reached here")
    if request.method == 'GET':
        session.clear()
        print("++++++ login form")
        form_login = LoginForm()
        print("+++++++ form_login")
        return render_template("login.html", form=form_login, error=False)

    # POST
    if request.method == "POST":
        form_login = LoginForm(request.form)
        if form_login.validate():
            username = request.form.get("username")
            password = request.form.get("password")
            checkbox = request.form.get("checkbox")

            # safety check
            if not validate.validate_field(username):
                return render_template("login.html", form=form_login, error=True, error_message="Username is invalid "
                                                                                                ": (")
            if not validate.validate_field(password):
                return render_template("login.html", form=form_login, error=True, error_message="Password is invalid :(")

            # check username and password
            user = User.query.filter_by(username=username).first()
            if not user:
                return render_template("login.html", form=form_login, error=True, error_message="information wrong: (")

            if user.username != username:
                return render_template("login.html", form=form_login, error=True, error_message="invalid username")

            pass_db = user.password
            if not check_password_hash(pass_db, password):
                return render_template("login.html", form=form_login, error=True, error_message="invalid password")

            # add user id in db to user session
            session["user_id"] = user.id

            # check its first time user log in to website to show welcome message
            if user.new_user == 0:
                user.new_user = 1
                db.session.commit()

                flash(f"Welcome Dear {user.username}")
                first = validate.first_login
                return redirect('/')
            else:
                return redirect('/')
        else:
            return render_template("login.html", form=form_login, error=True, error_message="Invalid Inputs")


@user_endpoints.route("/register", methods=['GET', 'POST'])
def register():

    # GET
    if request.method == 'GET':
        form = RegisterForm()
        return render_template("register.html", form=form, error=False)

    # POST
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate():
            username = request.form.get("username")
            password = request.form.get("password")
            password_re = request.form.get("password_re")

            # safety check
            if not validate.validate_field(username):
                return render_template("register.html", form=form, error=True, error_message="Username is invalid")

            password_validation = validate.validate_passwords(password, password_re)
            if password_validation == "NS":
                return render_template("register.html", form=form, error=True, error_message="Password does not match")
            elif not password_validation:
                return render_template("register.html", form=form, error=True, error_message="Password is wrong")

            # check user is not duplicated
            user_check = User.query.filter_by(username=username).first()
            if user_check:
                return render_template("register.html", form=form, error=True, error_message="Username Already take "
                                                                                             "by another User")

            # add it ro to database
            new_user = User(username=username, password=generate_password_hash(password=password))
            db.session.add(new_user)
            db.session.commit()

            # query to database
            user_in_db = User.query.filter_by(username=username).first()
            if not user_in_db:
                return error_500_server()

            # add first column(welcome message to user task column)
            new_task = Task(user_id=user_in_db.id, task_title=validate.first_login[1], task_description=validate.first_login[2])
            db.session.add(new_task)
            db.session.commit()

            flash(f"Register complete {username}")
            return redirect('login')
        else:
            return render_template("register.html", form=form, error=True, error_message="Invalid Inputs")
