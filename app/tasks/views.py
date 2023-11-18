from flask import Blueprint, jsonify, request
from app.init import db
from app.models import User, Task

tasks_blueprint = Blueprint('tasks', __name__)

@tasks_blueprint.route('/add', methods=['POST'])
def add_task():
    description = request.json.get('description', '')
    new_task = Task(description=description)
    db.session.add(new_task)
    db.session.commit()

    # Attempt to assign the task
    assign_task_to_user(new_task)

    return jsonify({'message': 'Task added successfully', 'task_id': new_task.id}), 201

@tasks_blueprint.route('/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.status == 'in_progress':
        task.status = 'completed'
        user = User.query.get(task.assigned_to)
        user.status = 'free'
        db.session.commit()

        # Attempt to assign new task to the user
        assign_new_task_to_user(user)

        return jsonify({'message': 'Task completed successfully'}), 200
    else:
        return jsonify({'message': 'Task not found or not in progress'}), 404

@tasks_blueprint.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_data = [{'id': task.id, 'description': task.description, 'status': task.status} for task in tasks]
    return jsonify({'tasks': tasks_data}), 200

def assign_task_to_user(task):
    user = User.query.filter_by(is_logged_in=True, status='free').first()
    if user:
        task.assigned_to = user.id
        task.status = 'in_progress'
        user.status = 'busy'
        db.session.commit()

def assign_new_task_to_user(user):
    if user.status == 'free':
        new_task = Task.query.filter_by(status='unassigned').first()
        if new_task:
            new_task.assigned_to = user.id
            new_task.status = 'in_progress'
            user.status = 'busy'
            db.session.commit()