import face_recognition
import os
import pickle

class FaceTrainingEngine:
    def __init__(self, images_path='student_images', encodings_file='encodings.pickle'):
        self.images_path = images_path
        self.encodings_file = encodings_file

    def train(self):
        print("[TRAINING] Starting the face training process...")
        known_encodings = []
        known_ids = []

        student_id_folders = [f for f in os.listdir(self.images_path) if os.path.isdir(os.path.join(self.images_path, f))]

        if not student_id_folders:
            print("[ERROR] No student image folders found in 'student_images/'.")
            return

        for student_id in student_id_folders:
            print(f"[INFO] Processing images for student ID: {student_id}")
            student_folder_path = os.path.join(self.images_path, student_id)
            image_files = [f for f in os.listdir(student_folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            
            if not image_files:
                print(f"[WARNING] No images found for student {student_id}. Skipping.")
                continue

            for image_file in image_files:
                image_path = os.path.join(student_folder_path, image_file)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    known_encodings.append(encodings[0])
                    known_ids.append(student_id)
                else:
                    print(f"[WARNING] No face found in {image_file}. Skipping.")

        if not known_encodings:
            print("[ERROR] Training failed. No faces were encoded.")
            return

        print("\n[INFO] Saving encodings to disk...")
        data = {"encodings": known_encodings, "ids": known_ids}
        with open(self.encodings_file, 'wb') as f:
            pickle.dump(data, f)
            
        print(f"[SUCCESS] Training complete. {len(known_encodings)} faces encoded.")