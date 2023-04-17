from functools import wraps
from flask import request, redirect, url_for
from flask import render_template, session

first_login = [0, "Welcome to ToDo-APP".title(), 'Planning, list your work and Do best'.title()]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def validate_field(string):
    """take a `field` and validate it"""
    if not string:
        return False
    for i in string:
        if i == "_" or i.isdigit() or i.isalpha():
            continue
        else:
            return False
    return True


def validate_passwords(password1, password2):
    """validate multi input passwords"""
    if not validate_field(password1):
        return False
    if not validate_field(password2):
        return False
    if password1 != password2:
        # Not Same
        return "NS"
    return True


def validate_tasks(task):
    if not task.strip():
        return False
    return True
