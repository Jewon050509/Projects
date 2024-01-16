from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Task
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

# Route for todo page
@views.route('/', methods=['GET', 'POST'])
@login_required
def todo():
    # Receives Task info from HTML
    if request.method == 'POST': 
        task = request.form.get('task')
        due_date_str = request.form.get('due_date')
        due_date = None

        if due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')

        # Create a new Task and add it to the database
        new_task = Task(data=task, due_date=due_date, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added!', category='success')

        return redirect(url_for('views.todo'))
    
    return render_template("todo.html", user=current_user)

# Route for deleting task
@views.route('/delete-task', methods=['POST'])
def delete_task():
    task = json.loads(request.data)
    taskId = task['taskId']
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()

    flash('Task removed!', category='error')

    return jsonify({})