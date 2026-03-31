import sqlite3
import os
import sys

def get_app_path():
    if getattr(sys, 'frozen', False):
        # Running as EXE
        return os.path.dirname(sys.executable)
    else:
        # Running as Python
        return os.path.dirname(os.path.abspath(__file__))

class Memory:
    def __init__(self):
        self.conn = sqlite3.connect(
            os.path.join(get_app_path(), "jarvis_memory.db"),
            check_same_thread=False   # ✅ KEY FIX
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        self.conn.commit()

    def remember(self, key, value):
        self.cursor.execute(
            "INSERT OR REPLACE INTO memory VALUES (?, ?)",
            (key, value)
        )
        self.conn.commit()

    def recall(self, key):
        self.cursor.execute(
            "SELECT value FROM memory WHERE key=?",
            (key,)
        )
        row = self.cursor.fetchone()
        return row[0] if row else None
