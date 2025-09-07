
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
from .modals import User, Tasks
from datetime import datetime
import json

main = Blueprint("main", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route("/", methods=['GET', 'POST'])
def login_page():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user, remember=False)
            return redirect(url_for("main.index"))
        flash("Invalid username or password", "error")
        return render_template("login.html")
    return render_template("login.html")

@main.route("/register", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
             flash("Username and password are required!", "error")
             return render_template("/register.html")
        if User.query.filter_by(username=username).first():
            flash("Username is already taken!", 'error')
            return render_template("register.html")
        new_user = User(username=username, password_hash = generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("main.login_page"))
    return render_template("register.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Thank you for using my ToDo app!")
    return render_template("login.html")

from collections import defaultdict

@main.route("/index")
@login_required
def index():
    all_tasks = Tasks.query.order_by(Tasks.priority).all()

    # Group tasks by priority
    tasks_by_priority = defaultdict(list)
    for task in all_tasks:
        tasks_by_priority[task.priority].append(task)

    return render_template("index.html", tasks_by_priority=tasks_by_priority)


@main.route("/create_task", methods=["GET", "POST"])
@login_required
def create_tasks():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        priority = int(request.form.get("priority"))
        due_datestr = request.form.get("due_date")
        due_date = datetime.strptime(due_datestr, "%Y-%m-%d") if due_datestr else None
        tags = request.form.getlist("tags")
        tags_json = json.dumps(tags)

        new_task = Tasks(
            title=title,
            content=content,
            priority=priority,
            due_date=due_date,
            tag=tags_json,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("main.index"))

    return render_template("create_task.html")


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

@main.route("/edit_task", methods=["POST"])
@login_required
def edit_task():
    task_id = request.form.get("task_id")
    task = Tasks.query.get(task_id)
    if not task or task.user_id != current_user.id:
        flash("Task not found or not authorized!", "error")
        return redirect(url_for("main.index"))

    task.title = request.form.get("title")
    task.content = request.form.get("content")
    task.priority = int(request.form.get("priority"))
    due_date = request.form.get("due_date")
    task.due_date = datetime.strptime(due_date, "%y-%m-%d") if due_date else None
    tags = request.form.getlist("tags[]")
    task.tag = json.dumps(tags)

    db.session.commit()
    flash("Task updated successfully!", "success")
    return redirect(url_for("main.index"))

@main.route("/start_task/<int:task_id>", methods=["POST"])
@login_required
def start_task(task_id):
    task = Tasks.query.get(task_id)
    if not task or task.user_id != current_user.id:
        flash("Task not found or not autherized!", "error")
        return redirect(url_for("main.index"))
    task.status = task.status.__class__.in_progress
    db.session.commit()
    flash(f"Task {task.title}' started!", "succes")
    return redirect(url_for("main.index"))

@main.route("/done_task/<int:task_id>", methods=["POST"])
@login_required
def done_task(task_id):
    task = Tasks.query.get(task_id)
    if not task or task.user_id != current_user.id:
        flash("Task not found or not autherized!", "error")
        return redirect(url_for("main.index"))
    task.status = task.status.__class__.completed
    db.session.commit()
    flash(f"Task {task.title}' started!", "succes")
    return redirect(url_for("main.index"))