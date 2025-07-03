# 🎯 Advance Attendance System

An intelligent face recognition–powered attendance solution with a live dashboard and real-time video stream. Built using OpenCV, MediaPipe, and Flask, this project blends computer vision and web technologies to create a fully functional desktop attendance system.

---

## ✨ Features

* 📸 **Real-Time Face Recognition** using OpenCV and MediaPipe
* 🖥️ **Desktop UI** for starting, stopping, and viewing attendance
* 🧾 **Attendance Logging** to CSV with time and name tracking
* 📊 **Live Web Dashboard** via Flask to monitor recognized faces
* 💾 **Local Storage** for known face encodings
* 🧠 **Easy to Train**: Just add face images to the folder, and the system learns them

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat\&logo=python\&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-27338E?style=flat\&logo=opencv\&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-F57C00?style=flat\&logo=google\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat\&logo=flask\&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=flat)

---

## 🚀 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/Zaid2044/Advance-Attendence-system.git
cd Advance-Attendence-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install manually:

```bash
pip install opencv-python mediapipe flask numpy
```

### 3. Add Training Images

* Add clear front-facing face images to the `known_faces/` directory.
* The filename (without extension) will be treated as the name of the person.

### 4. Run the System

```bash
python app.py
```

Then open your browser at: [http://localhost:5000](http://localhost:5000)

---

## 🧪 Demo Preview

Coming soon — add screenshots of:

* Face recognition UI
* Attendance logs
* Live dashboard

---

## 📁 Project Structure

```
Advance-Attendence-system/
├── app.py
├── known_faces/
├── static/
│   └── styles.css
├── templates/
│   └── dashboard.html
├── attendance.csv
└── requirements.txt
```

---

## 🧑‍💻 Author

** MOHAMMED ZAID AHMED**
[![GitHub](https://img.shields.io/badge/GitHub-Zaid2044-181717?style=flat\&logo=github)](https://github.com/Zaid2044)

---

## 🪪 License

MIT License
