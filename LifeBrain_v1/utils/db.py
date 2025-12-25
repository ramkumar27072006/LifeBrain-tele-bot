# utils/db.py
import sqlite3
DB_PATH = "lifebrain.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task TEXT,
        time TEXT
    );
    """)
    conn.commit()
    conn.close()

def add_task(user_id, task, time):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (user_id, task, time) VALUES (?, ?, ?)", (user_id, task, time))
    conn.commit()
    conn.close()

def get_tasks(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT task, time FROM tasks WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def delete_task(user_id: int, task_index: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM tasks WHERE user_id=? ORDER BY id",
        (user_id,)
    )
    rows = cursor.fetchall()

    if task_index < 1 or task_index > len(rows):
        conn.close()
        return False

    task_id = rows[task_index - 1][0]
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return True
