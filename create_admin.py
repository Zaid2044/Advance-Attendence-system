from database_manager import DatabaseManager
from werkzeug.security import generate_password_hash
import getpass

def create_initial_admin():
    db = DatabaseManager()
    
    print("--- Create Initial Admin User ---")
    username = input("Enter admin username: ").strip()

    if not username:
        print("Username cannot be empty.")
        db.close()
        return

    existing_user = db.get_user(username)
    if existing_user:
        print(f"\nError: A user with the username '{username}' already exists.")
        print("Please run the script again with a different username if you need to create another admin.")
        db.close()
        return

    print(f"Creating new admin user: '{username}'")
    password = getpass.getpass("Enter admin password: ")
    
    if not password:
        print("Password cannot be empty.")
        db.close()
        return
        
    hashed_password = generate_password_hash(password)
    
    try:
        db.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        db.conn.commit()
        print(f"\nAdmin user '{username}' created successfully.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    create_initial_admin()