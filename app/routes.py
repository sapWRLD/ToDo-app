
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from .modals import User, Tasks

main = Blueprint("main", __name__)

@login_manager._load_user
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route("/", methods=['GET', 'POST'])
def login_page():
    return render_template("login.html")

@main.route("/create_account")
def create_user():
    return render_template("/create_user.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    message = "Thank you for using my ToDo app!"
    return render_template("/login.html", message=message)