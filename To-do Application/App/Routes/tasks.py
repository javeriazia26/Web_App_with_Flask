from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db  #importng db object from app package to perform database operations
from app.models import Task 

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks') #creating object for blueprint

@tasks_bp.route('/task', methods=['GET', 'POST'])
def view_tasks():
    if 'user_id' not in session:
        flash('Please log in to view tasks.', 'warning')
        return redirect(url_for('auth.login'))
        
    task = Task.query.filter_by(user_id=session["user_id"]).all() # Retrieve all tasks from the database
    return render_template('tasks.html', tasks = task)

@tasks_bp.route('/add', methods=['POST'])
def add_tasks():
    if 'user_id' not in session:
        flash('Please log in to add tasks.', 'warning')
        return redirect(url_for('auth.login'))

    title = request.form['title'] 
    if title:
        new_task = Task(title=title, status = 'Pending', user_id=session["user_id"])  # Create a new task instance for specifix user
        db.session.add(new_task)  # Add the new task to the session
        db.session.commit()  # Commit the session to save the task to the database
        flash('Task added successfully!', 'success')
    else:
        flash('Task title cannot be empty.', 'error')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_tasks(task_id):
    task = Task.query.filter_by(id=task_id, user_id=session["user_id"]).first() # Retrieve the task by its ID and user id
    if task:
        if task.status == 'Pending':
            task.status = 'In Progress'

        elif task.status == 'In Progress':
            task.status = 'Completed'
        else:
            task.status = 'Pending'
        db.session.commit()  # Commit the session to save the updated task status
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():
    Task.query.filter_by(user_id=session["user_id"]).delete()  # Delete all tasks from the database
    db.session.commit() # Commit the session to save the changes

    flash('All tasks cleared successfully!', 'success')
    return redirect(url_for('tasks.view_tasks'))