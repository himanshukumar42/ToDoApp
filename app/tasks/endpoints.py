from flask import Blueprint, request, render_template, redirect, session, flash
from app.utility.validate import login_required
from app.tasks.models import Task

from application import db
import app.utility.validate as validate

task_endpoints = Blueprint('task_endpoints', __name__)


@task_endpoints.errorhandler(500)
def error_500_server(e):
    return render_template('500.html'), 500


@task_endpoints.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@task_endpoints.route("/health")
def health_check():
    return "<h1>Health Check: Ok</h1>"


@task_endpoints.route('/add_new_task', methods=['POST'])
@login_required
def add_new_task():
    title = request.form.get("task_title")
    description = request.form.get("task_description")

    if not validate.validate_tasks(title):
        return redirect('/')
    if not validate.validate_tasks(description):
        return redirect('/')

    # add task to User db
    new_task = Task(user_id=session['user_id'], task_title=title, task_description=description)
    try:
        db.sesion.add(new_task)
        db.session.commit()
        flash("Task Added Successfully")
        return redirect('/')
    except Exception as e:
        print(str(e))
        return error_500_server()


@task_endpoints.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        return render_template('edit.html', post_id=request.args.get("post_id"))
    if request.method == 'POST':
        # edit section
        title = request.form.get("edit_task_title")
        description = request.form.get("edit_task_description")
        task_id = request.form.get("post_id")

        if not validate.validate_tasks(title):
            return redirect('/')
        if not validate.validate_tasks(description):
            return redirect('/')
        if not validate.validate_tasks(task_id):
            return redirect('/')

        try:
            new_task = Task.query.filter_by(id=task_id).first()
            if not new_task:
                return redirect('/')

            new_task.title = title.title()
            new_task.description = description.title()
            db.session.commit()
            flash("Task Edited successfully")
            return redirect('/')
        except Exception as e:
            print(str(e))
            return error_500_server()


@task_endpoints.route("/delete", methods=['GET', 'POST'])
@login_required
def delete_task():
    if request.method == 'GET':
        return render_template('delete.html', post_id=request.args.get('post_id'))
    if request.method == 'POST':
        if request.form.get('delete') == 'Yes':
            try:
                new_task = Task.query.filter_by(id=request.form.get('post_id'), user_id=session['user_id']).first()
                if new_task is None:
                    return redirect('/')
                db.session.delete(new_task)
                db.session.commit()
                flash("Task Deleted Successfully")
                return redirect('/')
            except Exception as e:
                print(str(e))
                flash(message="Invalid Task", category="error")
                return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')


@task_endpoints.route("/done", methods=['POST'])
@login_required
def complete_task():
    if request.method == 'POST':
        task_id = request.form.get("post_id")

        # query to database for change task status to done
        new_task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()

        if new_task is None:
            return redirect('/')

        # status code 1 equal to done
        new_task.status = 1
        print(new_task.status)
        print(new_task)
        db.session.commit()
        flash("Task Done. You can see your all done task in history section")
        return redirect('/')


@task_endpoints.route("/history")
@login_required
def history():
    # query to db to get all Done task
    old_task = Task.query.filter_by(status=1, user_id=session['user_id'])
    return render_template('history.html', user_db=old_task)
