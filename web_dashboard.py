# /AdvancedAttendanceSystem/web_dashboard.py

import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from database_manager import DatabaseManager
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-and-random-string'
socketio = SocketIO(app, message_queue='redis://127.0.0.1:6379')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    db = DatabaseManager()
    try:
        user_data = db.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    finally:
        db.close()
        
    if user_data:
        return User(id=user_data[0], username=user_data[1], password=user_data[2])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('daily_report'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db = DatabaseManager()
        try:
            user_data = db.get_user(username)
        finally:
            db.close()
            
        if user_data and check_password_hash(user_data[2], password):
            user = User(id=user_data[0], username=user_data[1], password=user_data[2])
            login_user(user)
            return redirect(url_for('daily_report'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def daily_report():
    report_date_str = request.form.get('report_date') or datetime.now().strftime('%Y-%m-%d')
    students = get_attendance_data(report_date_str)
    return render_template('report.html', students=students, date=report_date_str, username=current_user.username)

@socketio.on('attendance_update')
def handle_attendance_update(data):
    print(f'[WEBSOCKET RELAY] Received update for {data["student_id"]}, broadcasting.')
    socketio.emit('new_attendance_log', data, broadcast=True)

def get_attendance_data(report_date):
    db_manager = DatabaseManager()
    try:
        all_students_records = db_manager.get_all_students()
        if not all_students_records:
            return []
            
        students_data = {
            s[1]: {'student_id': s[1], 'name': s[2], 'class_name': s[4], 'status': 'A', 'timestamp': ''}
            for s in all_students_records
        }
        
        query = "SELECT s.student_id, a.status, a.timestamp FROM attendance a JOIN students s ON a.student_internal_id = s.id WHERE a.date = ?"
        db_manager.cursor.execute(query, (report_date,))
        present_students = db_manager.cursor.fetchall()
        
        for student_id, status, timestamp in present_students:
            if student_id in students_data:
                students_data[student_id]['status'] = status
                students_data[student_id]['timestamp'] = timestamp
    finally:
        db_manager.close()
        
    return sorted(list(students_data.values()), key=lambda x: x['name'])

if __name__ == '__main__':
    print("--- Starting Web Dashboard ---")
    print("Access the dashboard at: http://127.0.0.1:5000")
    print("----------------------------")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)