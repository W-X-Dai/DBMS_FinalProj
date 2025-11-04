import psycopg2
from passlib.hash import bcrypt
from utils import list_students

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
    if bcrypt.verify(password, hashed_pw):
        print(f"WELCOME BACK, {name}")
    else:
        print("PASSWORD INCORRECT")

# === MAIN LOOP ===
def main():
    while True:
        print("\n--- STUDENT LOGIN SYSTEM ---")
        print("1. REGISTER")
        print("2. LOGIN")
        print("3. EXIT")
        choice = input("PLEASE SELECT AN OPTION: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("SYSTEM EXIT")
            break
        elif choice == "4":
            print(list_students())

        else:
            print("PLEASE SELECT A VALID OPTION")

if __name__ == "__main__":
    main()
