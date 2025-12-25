# utils/memory.py
import sqlite3
DB_PATH = "lifebrain.db"

def init_memory():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            city TEXT,
            language TEXT,
            chatmode TEXT
        )
        """)
        conn.commit()

def set_user_pref(user_id, field, value):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM memory WHERE user_id=?", (user_id,))
        if cur.fetchone():
            cur.execute(f"UPDATE memory SET {field}=? WHERE user_id=?", (value, user_id))
        else:
            cur.execute("INSERT INTO memory (user_id, name, city, language, chatmode) VALUES (?, '', '', '', 'default')", (user_id,))
            cur.execute(f"UPDATE memory SET {field}=? WHERE user_id=?", (value, user_id))
        conn.commit()

def get_user_pref(user_id, field):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT {field} FROM memory WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        return row[0] if row and row[0] is not None else None
