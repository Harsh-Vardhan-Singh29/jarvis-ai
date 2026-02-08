import sqlite3

class Memory:
    def __init__(self):
        self.conn = sqlite3.connect(
            "jarvis_memory.db",
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
