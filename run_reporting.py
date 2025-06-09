import pandas as pd
from database_manager import DatabaseManager
from datetime import datetime
import os

class ReportingEngine:
    def __init__(self, reports_dir='reports/'):
        self.db_manager = DatabaseManager()
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_daily_report(self, report_date=None):
        if report_date is None:
            report_date = datetime.now().strftime('%Y-%m-%d')
        
        print(f"\n--- Generating Attendance Report for {report_date} ---")

        all_students_records = self.db_manager.get_all_students()
        if not all_students_records:
            print("[ERROR] No students found in the database.")
            self.db_manager.close()
            return
            
        all_students_dict = [{'student_id': s[1], 'name': s[2], 'class_name': s[4]} for s in all_students_records]
        report_df = pd.DataFrame(all_students_dict)
        report_df['date'] = report_date
        report_df['status'] = 'A'
        report_df['timestamp'] = ''

        query = """
        SELECT s.student_id, a.status, a.timestamp
        FROM attendance a JOIN students s ON a.student_internal_id = s.id
        WHERE a.date = ?
        """
        self.db_manager.cursor.execute(query, (report_date,))
        present_students = self.db_manager.cursor.fetchall()
        
        if present_students:
            print(f"Found {len(present_students)} present students for this date.")
            for student_id, status, timestamp in present_students:
                report_df.loc[report_df['student_id'] == student_id, 'status'] = status
                report_df.loc[report_df['student_id'] == student_id, 'timestamp'] = timestamp
        else:
            print("No students were marked present on this date.")

        report_df = report_df[['student_id', 'name', 'class_name', 'date', 'status', 'timestamp']]
        file_name = f"Attendance_Report_{report_date}.xlsx"
        file_path = os.path.join(self.reports_dir, file_name)
        
        try:
            report_df.to_excel(file_path, index=False, engine='openpyxl')
            print(f"\n[SUCCESS] Report generated: {file_path}")
        except Exception as e:
            print(f"\n[ERROR] Could not save Excel file: {e}")
        
        self.db_manager.close()