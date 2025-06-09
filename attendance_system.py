import cv2
import face_recognition
import pickle
from datetime import datetime
from database_manager import DatabaseManager
import numpy as np
import socketio

class LiveAttendanceSystem:
    def __init__(self, stop_event):
        self.stop_event = stop_event
        self.db_manager = DatabaseManager()
        
        self.sio = socketio.Client()
        try:
            self.sio.connect('http://127.0.0.1:5000')
            print("[INFO] Connected to WebSocket server for live updates.")
        except socketio.exceptions.ConnectionError:
            print("[WARNING] Could not connect to WebSocket server. Live web updates will be disabled.")
            self.sio = None

        try:
            with open('encodings.pickle', 'rb') as f:
                self.known_data = pickle.load(f)
        except FileNotFoundError:
            print("[ERROR] Encodings file not found."); self.known_data = None; return

        self.known_encodings = self.known_data["encodings"]
        self.known_ids = self.known_data["ids"]
        
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            print("[ERROR] Cannot open webcam."); return

        self.todays_present_ids = set()
        print("[SETUP] Initialization complete. Starting recognition...")

    def run_recognition(self):
        if not self.known_data or not self.video_capture.isOpened():
            print("[ERROR] System not initialized properly."); return

        while not self.stop_event.is_set():
            ret, frame = self.video_capture.read()
            if not ret: break

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=0.5)
                display_name = "Unknown"; student_info_text = ""
                face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    student_id = self.known_ids[best_match_index]
                    if student_id not in self.todays_present_ids:
                        student_info = self.db_manager.get_student_by_id(student_id)
                        if student_info:
                            current_date = datetime.now().strftime('%Y-%m-%d')
                            current_time = datetime.now().strftime('%H:%M:%S')
                            if self.db_manager.log_attendance(student_info['id'], current_date, 'P', current_time):
                                print(f"[LOGGED] Attendance for {student_info['name']} logged.")
                                self.todays_present_ids.add(student_id)
                                if self.sio and self.sio.connected:
                                    update_data = {'student_id': student_info['student_id'], 'status': 'P', 'timestamp': current_time}
                                    self.sio.emit('attendance_update', update_data)
                                    print(f"[WEBSOCKET] Sent update for {student_info['name']}.")

                    student_info = self.db_manager.get_student_by_id(student_id)
                    if student_info:
                        display_name = student_info['name']
                        student_info_text = f"Age: {student_info['age']} | Class: {student_info['class_name']}"

                top, right, bottom, left = (c * 4 for c in face_location)
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 60), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, display_name, (left + 6, bottom - 35), font, 0.7, (255, 255, 255), 1)
                cv2.putText(frame, student_info_text, (left + 6, bottom - 10), font, 0.5, (255, 255, 255), 1)

            cv2.imshow('Live Attendance System - Press "q" to close', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        self.video_capture.release()
        cv2.destroyAllWindows()
        self.db_manager.close()
        if self.sio and self.sio.connected: self.sio.disconnect()
        self.stop_event.set()
        print("[INFO] Live attendance system shut down.")