import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path='database/attendance.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            class_name TEXT NOT NULL
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_internal_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            UNIQUE(student_internal_id, date),
            FOREIGN KEY (student_internal_id) REFERENCES students (id) ON DELETE CASCADE
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def get_user(self, username):
        """Fetches a user by their username."""
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def add_student(self, student_data):
        query = "INSERT INTO students (student_id, name, age, class_name) VALUES (?, ?, ?, ?)"
        try:
            self.cursor.execute(query, (
                student_data['student_id'],
                student_data['name'],
                student_data['age'],
                student_data['class_name']
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print(f"Error: Student ID '{student_data['student_id']}' already exists.")
            return False
            
    def update_student(self, internal_id, updated_data):
        query = "UPDATE students SET student_id = ?, name = ?, age = ?, class_name = ? WHERE id = ?"
        try:
            self.cursor.execute(query, (
                updated_data['student_id'],
                updated_data['name'],
                updated_data['age'],
                updated_data['class_name'],
                internal_id
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error during update: {e}")
            return False

    def get_student_by_id(self, student_id):
        self.cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        record = self.cursor.fetchone()
        if record:
            return {'id': record[0], 'student_id': record[1], 'name': record[2], 'age': record[3], 'class_name': record[4]}
        return None

    def get_all_students(self):
        self.cursor.execute("SELECT * FROM students ORDER BY name")
        return self.cursor.fetchall()

    def log_attendance(self, student_internal_id, date, status, timestamp):
        query = "INSERT OR IGNORE INTO attendance (student_internal_id, date, status, timestamp) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (student_internal_id, date, status, timestamp))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.conn.close()