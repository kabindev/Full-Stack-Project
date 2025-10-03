from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from functools import wraps
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productivity.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-use-os-urandom'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')
    habits = db.relationship('Habit', backref='user', lazy=True, cascade='all, delete-orphan')
    settings = db.relationship('UserSettings', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='pending')
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'completed_at': self.completed_at.strftime('%Y-%m-%d %H:%M:%S') if self.completed_at else None
        }

class Habit(db.Model):
    __tablename__ = 'habits'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    streak = db.Column(db.Integer, default=0)
    last_done_date = db.Column(db.Date, nullable=True)
    frequency = db.Column(db.String(20), default='daily')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    done_today = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'streak': self.streak,
            'last_done_date': self.last_done_date.strftime('%Y-%m-%d') if self.last_done_date else None,
            'frequency': self.frequency,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'done_today': self.done_today
        }

class DailyStreak(db.Model):
    """Track consecutive days when ALL habits are completed"""
    __tablename__ = 'daily_streaks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    all_habits_completed = db.Column(db.Boolean, default=False)

class UserSettings(db.Model):
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    theme = db.Column(db.String(20), default='light')
    motivational_message = db.Column(db.String(500), default='Keep going! You are doing great!')

# Initialize database
with app.app_context():
    db.create_all()

# Authentication Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Helper Functions
def calculate_productivity_score(user_id):
    """Calculate productivity score for a specific user"""
    tasks_completed = Task.query.filter_by(user_id=user_id, status='completed').count()
    total_streak_days = get_total_streak_days(user_id)
    return (tasks_completed * 10) + (total_streak_days * 5)

def get_total_streak_days(user_id):
    """
    Calculate consecutive days where ALL habits were completed for a specific user.
    """
    today = datetime.now().date()
    habits = Habit.query.filter_by(user_id=user_id).all()
    
    if len(habits) == 0:
        return 0
    
    streak_days = 0
    current_date = today
    
    for _ in range(365):
        habits_done_on_date = sum(1 for h in habits if h.last_done_date == current_date and h.done_today)
        
        if habits_done_on_date == len(habits):
            streak_days += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak_days

def check_all_habits_completed_today(user_id):
    """Check if all habits are completed today and update daily streak"""
    today = datetime.now().date()
    habits = Habit.query.filter_by(user_id=user_id).all()
    
    if len(habits) == 0:
        return False
    
    all_done = all(habit.done_today for habit in habits)
    
    daily_record = DailyStreak.query.filter_by(user_id=user_id, date=today).first()
    if not daily_record:
        daily_record = DailyStreak(user_id=user_id, date=today, all_habits_completed=all_done)
        db.session.add(daily_record)
    else:
        daily_record.all_habits_completed = all_done
    
    db.session.commit()
    return all_done

def check_and_reset_streaks():
    """Reset streaks if habits weren't done yesterday - for all users"""
    with app.app_context():
        today = datetime.now().date()
        habits = Habit.query.all()
        
        for habit in habits:
            if habit.last_done_date:
                days_diff = (today - habit.last_done_date).days
                if days_diff > 1:
                    habit.streak = 0
                    habit.done_today = False
            
            if habit.last_done_date != today:
                habit.done_today = False
        
        db.session.commit()

# Authentication Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index2.html')
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    
    # Validation
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(data['username']) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    
    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Create default settings for user
    settings = UserSettings(user_id=user.id)
    db.session.add(settings)
    db.session.commit()
    
    session['user_id'] = user.id
    session['username'] = user.username
    
    return jsonify({'message': 'Registration successful', 'username': user.username}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    session['user_id'] = user.id
    session['username'] = user.username
    
    return jsonify({'message': 'Login successful', 'username': user.username}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/current-user', methods=['GET'])
@login_required
def current_user():
    user = User.query.get(session['user_id'])
    return jsonify({'username': user.username, 'email': user.email})

# API Routes (Protected)
@app.route('/api/dashboard', methods=['GET'])
@login_required
def get_dashboard():
    user_id = session['user_id']
    
    total_tasks = Task.query.filter_by(user_id=user_id).count()
    completed_tasks = Task.query.filter_by(user_id=user_id, status='completed').count()
    
    habits = Habit.query.filter_by(user_id=user_id).all()
    active_habits = len(habits)
    
    total_streak_days = get_total_streak_days(user_id)
    productivity_score = calculate_productivity_score(user_id)
    
    return jsonify({
        'productivity_score': productivity_score,
        'tasks_completed': completed_tasks,
        'total_tasks': total_tasks,
        'total_streak_days': total_streak_days,
        'active_habits': active_habits
    })

@app.route('/api/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    user_id = session['user_id']
    
    if request.method == 'GET':
        tasks = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()
        return jsonify([task.to_dict() for task in tasks])
    
    elif request.method == 'POST':
        data = request.json
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
            except:
                pass
        
        task = Task(
            user_id=user_id,
            title=data['title'],
            due_date=due_date
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
@login_required
def task_detail(task_id):
    user_id = session['user_id']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    
    if request.method == 'PUT':
        data = request.json
        if 'status' in data:
            task.status = data['status']
            if data['status'] == 'completed':
                task.completed_at = datetime.utcnow()
            else:
                task.completed_at = None
        if 'title' in data:
            task.title = data['title']
        db.session.commit()
        return jsonify(task.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'}), 200

@app.route('/api/habits', methods=['GET', 'POST'])
@login_required
def habits():
    user_id = session['user_id']
    
    if request.method == 'GET':
        habits = Habit.query.filter_by(user_id=user_id).order_by(Habit.created_at.desc()).all()
        return jsonify([habit.to_dict() for habit in habits])
    
    elif request.method == 'POST':
        data = request.json
        if not data.get('name'):
            return jsonify({'error': 'Habit name is required'}), 400
        
        habit = Habit(
            user_id=user_id,
            name=data['name'],
            frequency=data.get('frequency', 'daily')
        )
        db.session.add(habit)
        db.session.commit()
        return jsonify(habit.to_dict()), 201

@app.route('/api/habits/<int:habit_id>', methods=['PUT', 'DELETE'])
@login_required
def habit_detail(habit_id):
    user_id = session['user_id']
    habit = Habit.query.filter_by(id=habit_id, user_id=user_id).first_or_404()
    
    if request.method == 'PUT':
        data = request.json
        today = datetime.now().date()
        
        if 'mark_done' in data and data['mark_done']:
            if not habit.done_today:
                if habit.last_done_date:
                    days_diff = (today - habit.last_done_date).days
                    if days_diff == 1:
                        habit.streak += 1
                    elif days_diff > 1:
                        habit.streak = 1
                    else:
                        habit.streak = habit.streak
                else:
                    habit.streak = 1
                
                habit.last_done_date = today
                habit.done_today = True
                
                check_all_habits_completed_today(user_id)
        
        if 'name' in data:
            habit.name = data['name']
        
        db.session.commit()
        return jsonify(habit.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(habit)
        db.session.commit()
        return jsonify({'message': 'Habit deleted'}), 200

@app.route('/api/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user_id = session['user_id']
    user_setting = UserSettings.query.filter_by(user_id=user_id).first()
    
    if not user_setting:
        user_setting = UserSettings(user_id=user_id)
        db.session.add(user_setting)
        db.session.commit()
    
    if request.method == 'GET':
        return jsonify({
            'theme': user_setting.theme,
            'motivational_message': user_setting.motivational_message
        })
    
    elif request.method == 'POST':
        data = request.json
        if 'theme' in data:
            user_setting.theme = data['theme']
        if 'motivational_message' in data:
            user_setting.motivational_message = data['motivational_message']
        db.session.commit()
        return jsonify({
            'theme': user_setting.theme,
            'motivational_message': user_setting.motivational_message
        })

# Scheduler for streak checks
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_and_reset_streaks, trigger="cron", hour=0, minute=1)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True, port=5000)