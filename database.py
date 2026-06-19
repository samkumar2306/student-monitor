import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'school.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            group_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def get_members(group_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, phone FROM members WHERE group_type = ?", (group_type,))
    rows = c.fetchall()
    conn.close()
    return [{"name": r[0], "phone": r[1]} for r in rows]

def get_all_members():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, name, phone, group_type FROM members ORDER BY group_type, name")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "phone": r[2], "group": r[3]} for r in rows]

def add_member(name, phone, group_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO members (name, phone, group_type) VALUES (?, ?, ?)",
              (name, phone, group_type))
    conn.commit()
    conn.close()

def delete_member(member_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM members WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()