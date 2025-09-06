
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from .modals import User, Tasks
from datetime import datetime

main = Blueprint("main", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route("/", methods=['GET', 'POST'])
def login_page():
        if request.method == "POST":
            user = User.query.filter_by(user_name=request.form.get("username"))
            if user and check_password_hash(user.password_hash, request.form['password']):
                 login_user(user, remember=False)
                 return redirect(url_for("index"))
        
        return render_template("login.html")

@main.route("/register", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
             flash("Username and password are required!", "error")
             return render_template("/register")
        if User.query.filter_by(username=username).first():
            flash("Username is already taken!", 'error')
            render_template("/register.html")
        new_user = User(username=username, password_hash = generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        redirect(url_for("main.index"))
    return render_template("/register.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    message = "Thank you for using my ToDo app!"
    return render_template("/login.html", message=message)

@main.route("/index")
@login_required
def index():
    all_tasks = Tasks.query.all()
    render_template('/index.html', tasks=all_tasks)

@main.route("/create_task", methods=["GET", "POST"])
@login_required
def create_tasks():
     if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        priority = int(request.form.get("priority"))
        tags_list = request.form.getlist("tag")
        due_datestr = request.form["due_date"]
        due_date = datetime.strftime(due_datestr, "%Y-%m-%d") if due_datestr else None

        new_task = Tasks(
        title=title,
        content=content,
        priority=priority,
        due_date=due_date,
        tag=tags_list,  # store JSON array
        user_id=current_user.id
    )
        db.session.add(new_task)
        db.session.commit()
        return render_template("index.html")
     render_template("/create_task")

@main.route("/delete_task", methods=["POST"])
@login_required
def delete_task():
    task_id = request.form.get("id")
    task = Tasks.query.get(task_id)

    if task and task.user_id == current_user.id: 
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully")
    else:
        flash("Task not found or not authorized")

    return redirect(url_for("main.index"))

@main.route("/edit_tasks", methods=["POST"])
def edit_task():
    return render_template("/edit_task")
