import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "resource_system",
    "user": "postgres",
    "password": "test1234"
}

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

def list_students():
    conn = connect_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute("SELECT student_id, name, email FROM student ORDER BY student_id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def find_student_by_id(student_id):
    conn = connect_db()
    if not conn:
        return None
    cur = conn.cursor()
    cur.execute("SELECT student_id, name, email FROM student WHERE student_id = %s;", (student_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result