# Real-Time Face Recognition Attendance System

A robust, real-time attendance system that uses computer vision to detect and identify faces from a live webcam feed, automatically marking attendance and logging it with a timestamp.

---

### Core Features

- **Live Face Detection:** Utilizes OpenCV's Haar Cascade classifier for real-time face detection from a webcam stream.
- **Accurate Face Recognition:** Employs the `face_recognition` library (built on dlib) to compare detected faces against a database of known individuals.
- **Automated Attendance Logging:** When a known face is recognized, the system automatically records their name and the current timestamp into a CSV file.
- **Simple & Efficient UI:** A clean interface displays the live camera feed with bounding boxes and names drawn on recognized faces.

---

### Tech Stack

- **Primary Language:** Python
- **Computer Vision:** OpenCV (`opencv-python`)
- **Face Recognition:** `face_recognition` (dlib)
- **Data Handling:** Pandas, NumPy
- **Core Libraries:** `csv`, `datetime`

---

### Setup and Usage

1. **Clone the repository.**
2. **Create a folder named `ImagesAttendance`** and place images of the individuals you want to recognize inside. Name each image file with the person's name (e.g., `Name.jpg`).
3. **Install dependencies:**
   *(Note: Installing `dlib` and `face_recognition` can be complex. It may require installing `CMake` and C++ build tools first.)*
   ```bash
   pip install opencv-python numpy pandas face_recognition
   ```

---

1. **Run the application:**
  ```bash
   python main.py
  ```

2. **The system will open a webcam window. When a recognized person appears, their attendance will be logged in Attendance.csv.**
