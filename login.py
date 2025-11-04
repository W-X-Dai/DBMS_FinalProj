import psycopg2
from passlib.hash import bcrypt
from utils import list_students
from utils_redis import create_session, verify_session, delete_session


# === DATABASE CONFIGURATION ===
DB_CONFIG = {
    "host": "localhost",
    "database": "resource_system",
    "user": "postgres",
    "password": "test1234"
}

# === DATABASE CONNECTION ===
def connect_db():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        exit(1)

# === REGISTER ===
def register():
    print("\n=== REGISTER ===")
    sid = input("STUDENT_ID: ").strip()
    name = input("NAME: ").strip()
    email = input("Email: ").strip()
    password = input("PASSWORD: ").strip()

    hashed_pw = bcrypt.hash(password)

    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO student (student_id, name, email, password) VALUES (%s, %s, %s, %s)",
            (sid, name, email, hashed_pw)
        )
        conn.commit()
        print("Successfully registered!")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("STUDENT_ID or Email is already in use")
    finally:
        cur.close()
        conn.close()

# === LOGIN ===
def login():
    print("\n=== LOGIN ===")
    student_id = input("STUDENT_ID: ").strip()
    password = input("PASSWORD: ").strip()

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT password, name FROM student WHERE student_id=%s", (student_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        print("ACCOUNT NOT FOUND, PLEASE REGISTER FIRST")
        return

    hashed_pw, name = row
    if not bcrypt.verify(password, hashed_pw):
        print("PASSWORD INCORRECT")
        return

    token = create_session(student_id, "student")
    print(f"WELCOME BACK, {name}", f"TOKEN: {token}", sep="\n")

def check_session(student_id: str, token: str):
    if verify_session(student_id, token):
        print("SESSION VALID")
    else:
        print("SESSION INVALID OR EXPIRED")

def logout(student_id: str):
    delete_session(student_id)
    print("LOGGED OUT SUCCESSFULLY")

# === MAIN LOOP ===
def main():
    while True:
        print("\n--- STUDENT LOGIN SYSTEM ---")
        print("1. REGISTER")
        print("2. LOGIN")
        print("3. EXIT")
        print("4. LIST STUDENTS (FOR DEBUGGING PURPOSES)")
        choice = input("PLEASE SELECT AN OPTION: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("SYSTEM EXIT")
            break
        elif choice == "4":
            students = list_students()
            print("\n=== STUDENT LIST ===")
            print("STUDENT_ID \t| NAME \t| EMAIL")
            for student in students:
                print(f"{student[0]} \t| {student[1]} \t| {student[2]}")

        else:
            print("PLEASE SELECT A VALID OPTION")

if __name__ == "__main__":
    main()
