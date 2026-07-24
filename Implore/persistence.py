import sqlite3
import os
from path_resolver import resolver

class PersistenceManager:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = resolver.resolve("Implore/implore_data.db")
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._init_db()

    def _init_db(self):
        # Persistent storage for project profiles, history, and audit trails
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS project_profiles 
                             (id TEXT PRIMARY KEY, profile_json TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS grant_history 
                             (opp_id TEXT, success BOOLEAN, reasoning TEXT)''')
        self.conn.commit()

    def save_profile(self, profile_id, profile_json):
        self.cursor.execute('INSERT OR REPLACE INTO project_profiles VALUES (?, ?)', (profile_id, profile_json))
        self.conn.commit()

    def record_outcome(self, opp_id, success, reasoning):
        self.cursor.execute('INSERT INTO grant_history VALUES (?, ?, ?)', (opp_id, success, reasoning))
        self.conn.commit()
