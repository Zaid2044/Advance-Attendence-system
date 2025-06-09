![alt text](https://img.shields.io/badge/python-3.9+-blue.svg)


![alt text](https://img.shields.io/badge/status-complete-success.svg)


![alt text](https://img.shields.io/badge/license-MIT-green.svg)

A full-stack, AI-powered system designed to automate student attendance using real-time face recognition. The project features a Python backend, a multi-threaded Tkinter desktop application for administration, and a secure, live-updating web dashboard for viewing reports.

🌟 Core Features

🤖 AI-Powered Recognition: Automatically identifies registered students from a live webcam feed using the face_recognition library.

🖥️ Desktop Admin Panel: A user-friendly GUI built with Tkinter to manage student data (Add, Update, Delete), initiate AI model training, and control the live camera system.

🌐 Real-Time Web Dashboard: A secure, login-protected web dashboard built with Flask that displays attendance reports. The dashboard updates live using WebSockets as students are recognized.

📊 Historical Reporting: View attendance reports for any previous day using an interactive date picker on the web dashboard.

🔒 Secure Authentication: The web dashboard is protected by a full user login system with hashed passwords.

🚀 Professional Architecture: Utilizes a multi-threaded GUI to prevent freezing and a Redis message queue to facilitate robust communication between the desktop app and the web server.

📸 Demo

(It is highly recommended to add a GIF here showing the system in action: the camera recognizes a face, and the web dashboard updates instantly.)

🛠️ Technology Stack
Category	Technologies & Libraries
Backend	Python 3
AI & Computer Vision	face_recognition, dlib, OpenCV, Pillow, numpy
Desktop GUI	Tkinter
Web Framework	Flask, Flask-Login
Real-Time & Messaging	Flask-SocketIO, python-socketio, eventlet, Redis
Database	SQLite3
Data & Reporting	Pandas, openpyxl
Security	Werkzeug (for password hashing)
⚙️ Setup and Installation

Follow these steps to get the project running on your local machine.

1. Prerequisites

Python (version 3.9 or higher).

C++ Build Tools: Required by dlib. On Windows, install Visual Studio Build Tools with the "Desktop development with C++" workload.

Redis Server: Required for real-time web updates.

On Windows (Recommended): Install Redis via WSL (Windows Subsystem for Linux).

Install WSL: wsl --install (in an admin PowerShell).

Install Redis in your Linux distro: sudo apt update && sudo apt install redis-server

Start the service: sudo service redis-server start

On macOS: brew install redis && brew services start redis

2. Clone the Repository
git clone https://github.com/your-username/AdvancedAttendanceSystem.git
cd AdvancedAttendanceSystem

3. Install Dependencies

It's highly recommended to use a virtual environment.

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate    # On Windows

# Install all required packages
pip install -r requirements.txt

(You need to create a requirements.txt file with the content from the section below).

4. Initial Setup

Add Student Photos: Place images of students inside the student_images/ directory. Each student must have their own folder named with their unique Student ID (e.g., S-001, S-002).

Create Admin User: Run the script to create your first login credentials for the web dashboard. You will be prompted for a username and password.

python create_admin.py

▶️ How to Run

The system has two main components that need to be run in separate terminals.

Terminal 1: Start the Web Dashboard
python web_dashboard.py

Access the dashboard at http://127.0.0.1:5000

Terminal 2: Start the Desktop Admin Panel
python app_gui.py

Use the desktop app to manage students and start the live camera.


📜 License

This project is licensed under the MIT License.
