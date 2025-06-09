from database_manager import DatabaseManager

if __name__ == "__main__":
    db_manager = DatabaseManager()
    print("--- Database and tables created/verified. ---")
    
    student1 = {'student_id': 'S-001', 'name': 'Alice Smith', 'age': 16, 'class_name': 'Grade 10-A'}
    student2 = {'student_id': 'S-002', 'name': 'Bob Johnson', 'age': 17, 'class_name': 'Grade 11-B'}

    print("\n--- Adding sample students... ---")
    db_manager.add_student(student1)
    db_manager.add_student(student2)
    
    print("\n--- Listing all students... ---")
    all_students = db_manager.get_all_students()
    for student in all_students:
        print(student)

    db_manager.close()
    print("\n--- Initial setup complete. ---")