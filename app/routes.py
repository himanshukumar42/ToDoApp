from flask import Blueprint, current_app, render_template

root = Blueprint("root", __name__, template_folder='templates/')


@root.route("", methods=['GET'])
def health_check():
    return "<h1>Health Check: Ok</h1>"

