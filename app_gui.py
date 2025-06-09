import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import threading
import shutil
import stat

from database_manager import DatabaseManager
from face_training_engine import FaceTrainingEngine
from attendance_system import LiveAttendanceSystem
from run_reporting import ReportingEngine

class RedirectText:
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=tk.NORMAL)
        self.text_space.insert(tk.END, string)
        self.text_space.see(tk.END)
        self.text_space.config(state=tk.DISABLED)

    def flush(self):
        pass

class AppGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Advanced Attendance System")
        self.geometry("800x600")

        style = ttk.Style(self)
        style.map('Treeview', 
                  background=[('selected', '#347083')],
                  foreground=[('selected', 'white')])

        self.db_manager = DatabaseManager()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")
        
        self.stop_camera_event = threading.Event()
        self.camera_thread = None

        self.management_frame = ttk.Frame(self.notebook)
        self.operations_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.management_frame, text="Student Management")
        self.notebook.add(self.operations_frame, text="System Operations")

        self.create_management_widgets()
        self.create_operations_widgets()
        self.populate_student_list()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_management_widgets(self):
        list_frame = ttk.LabelFrame(self.management_frame, text="Student List")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("id", "student_id", "name", "age", "class_name")
        self.student_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.student_tree.heading(col, text=col.replace('_', ' ').title())
            self.student_tree.column(col, width=100)
        self.student_tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.student_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.student_tree.config(yscrollcommand=scrollbar.set)
        self.student_tree.bind("<<TreeviewSelect>>", self.on_student_select)
        
        form_frame = ttk.LabelFrame(self.management_frame, text="Student Details")
        form_frame.pack(fill="x", padx=10, pady=10)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(3, weight=1)

        ttk.Label(form_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.student_id_entry = ttk.Entry(form_frame)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(form_frame, text="Age:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.age_entry = ttk.Entry(form_frame)
        self.age_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        ttk.Label(form_frame, text="Class:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.class_entry = ttk.Entry(form_frame)
        self.class_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        button_frame = ttk.Frame(self.management_frame)
        button_frame.pack(fill="x", pady=10)
        ttk.Button(button_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Selected", command=self.update_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Add Photos for ID", command=self.add_photos).pack(side="left", padx=5)

    def create_operations_widgets(self):
        ops_container = ttk.Frame(self.operations_frame)
        ops_container.pack(fill='x', pady=20, padx=20)
        
        self.train_button = ttk.Button(ops_container, text="Run Face Training", command=self.run_training)
        self.train_button.pack(fill='x', pady=5)
        
        self.start_button = ttk.Button(ops_container, text="Start Live Attendance", command=self.start_live_attendance)
        self.start_button.pack(fill='x', pady=5)
        
        self.stop_button = ttk.Button(ops_container, text="Stop Live Attendance", command=self.stop_live_attendance, state=tk.DISABLED)
        self.stop_button.pack(fill='x', pady=5)
        
        self.report_button = ttk.Button(ops_container, text="Generate Daily Report", command=self.generate_report)
        self.report_button.pack(fill='x', pady=5)
        
        log_frame = ttk.LabelFrame(self.operations_frame, text="System Log")
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.log_text = tk.Text(log_frame, state=tk.DISABLED, wrap=tk.WORD, height=15)
        self.log_text.pack(fill="both", expand=True)
        sys.stdout = RedirectText(self.log_text)

    def populate_student_list(self):
        for item in self.student_tree.get_children(): self.student_tree.delete(item)
        for student in self.db_manager.get_all_students(): self.student_tree.insert("", "end", values=student)
            
    def clear_fields(self):
        self.student_id_entry.delete(0, tk.END); self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END); self.class_entry.delete(0, tk.END)
        self.student_tree.selection_remove(self.student_tree.selection())

    def add_student(self):
        student_data = {'student_id': self.student_id_entry.get(), 'name': self.name_entry.get(), 'age': self.age_entry.get(), 'class_name': self.class_entry.get()}
        if not all(student_data.values()):
            messagebox.showerror("Error", "All fields are required."); return
        if self.db_manager.add_student(student_data):
            messagebox.showinfo("Success", f"Student {student_data['name']} added. Now add their photos.")
            self.populate_student_list(); self.clear_fields()
        else:
            messagebox.showerror("Error", "Failed to add student. Check the log for details.")

    def on_student_select(self, event):
        self.student_id_entry.delete(0, tk.END); self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END); self.class_entry.delete(0, tk.END)
        selected_items = self.student_tree.selection()
        if not selected_items: return
        values = self.student_tree.item(selected_items[0], "values")
        if values:
            self.student_id_entry.insert(0, values[1]); self.name_entry.insert(0, values[2])
            self.age_entry.insert(0, values[3]); self.class_entry.insert(0, values[4])

    def update_student(self):
        selected_items = self.student_tree.selection()
        if not selected_items: messagebox.showerror("Error", "Please select a student to update."); return
        internal_id = self.student_tree.item(selected_items[0], "values")[0]
        updated_data = {'student_id': self.student_id_entry.get(), 'name': self.name_entry.get(), 'age': self.age_entry.get(), 'class_name': self.class_entry.get()}
        if not all(updated_data.values()): messagebox.showerror("Error", "All fields are required."); return
        if messagebox.askyesno("Confirm Update", "Are you sure you want to apply these changes?"):
            if self.db_manager.update_student(internal_id, updated_data):
                messagebox.showinfo("Success", "Student record updated successfully.")
                self.populate_student_list(); self.clear_fields()
            else:
                messagebox.showerror("Error", "Failed to update student. Check the log for details.")

    def delete_student(self):
        if not self.student_tree.selection(): messagebox.showerror("Error", "Please select a student to delete."); return
        student_id = self.student_tree.item(self.student_tree.selection()[0], "values")[1]
        if messagebox.askyesno("Confirm", f"Delete student {student_id}? This will also delete their image folder."):
            def remove_readonly(func, path, excinfo):
                os.chmod(path, stat.S_IWRITE)
                func(path)
            self.db_manager.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            self.db_manager.conn.commit()
            image_dir = os.path.join('student_images', student_id)
            if os.path.isdir(image_dir):
                try: shutil.rmtree(image_dir, onerror=remove_readonly)
                except Exception as e:
                    print(f"Error deleting folder {image_dir}: {e}")
                    messagebox.showerror("Deletion Error", f"Could not delete image folder.\nCheck log for details.")
                    return
            messagebox.showinfo("Success", f"Student {student_id} and their photos deleted.")
            self.populate_student_list(); self.clear_fields()
    
    def add_photos(self):
        student_id = self.student_id_entry.get()
        if not student_id: messagebox.showerror("Error", "Enter a student ID or select a student first."); return
        student_dir = os.path.join('student_images', student_id)
        os.makedirs(student_dir, exist_ok=True)
        files = filedialog.askopenfilenames(title='Select student photos', filetypes=[('Image Files', '*.jpg *.jpeg *.png')])
        if files:
            for i, file_path in enumerate(files):
                destination = os.path.join(student_dir, f"{student_id}_{i+1}{os.path.splitext(file_path)[1]}")
                shutil.copy(file_path, destination)
            messagebox.showinfo("Success", f"{len(files)} photos added for student {student_id}.")

    def run_training(self):
        threading.Thread(target=self._run_training_thread, daemon=True).start()
    
    def _run_training_thread(self):
        self.train_button.config(state=tk.DISABLED)
        print("--- Starting Face Training ---")
        FaceTrainingEngine().train()
        print("--- Face Training Complete ---")
        self.train_button.config(state=tk.NORMAL)

    def start_live_attendance(self):
        self.stop_camera_event.clear()
        self.camera_thread = threading.Thread(target=LiveAttendanceSystem(self.stop_camera_event).run_recognition, daemon=True)
        self.camera_thread.start()
        self.start_button.config(state=tk.DISABLED); self.stop_button.config(state=tk.NORMAL)
        self.check_camera_thread()

    def stop_live_attendance(self):
        if self.camera_thread and self.camera_thread.is_alive(): self.stop_camera_event.set()
        self.stop_button.config(state=tk.DISABLED)

    def check_camera_thread(self):
        if self.camera_thread and self.camera_thread.is_alive():
            self.after(100, self.check_camera_thread)
        else:
            self.start_button.config(state=tk.NORMAL); self.stop_button.config(state=tk.DISABLED)
            print("--- Live attendance thread has finished. ---")

    def generate_report(self):
        threading.Thread(target=self._generate_report_thread, daemon=True).start()
        
    def _generate_report_thread(self):
        self.report_button.config(state=tk.DISABLED)
        print("\n--- Generating Daily Report ---")
        ReportingEngine().generate_daily_report()
        print("--- Report Generation Finished ---\n")
        self.report_button.config(state=tk.NORMAL)
        
    def on_closing(self):
        if self.camera_thread and self.camera_thread.is_alive():
            self.stop_camera_event.set()
            self.camera_thread.join()
        self.destroy()

if __name__ == "__main__":
    app = AppGUI()
    app.mainloop()