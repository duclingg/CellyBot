import os
import sqlite3

from logger import CellyBotLogger

class FollowerStore:
    def __init__(self):
        self.logger = CellyBotLogger()
        
        # always resolve path relative to this file (in database/)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "followers.db")
        self.conn = sqlite3.connect(self.db_path)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS followers (
                username TEXT PRIMARY KEY
            )
        """)
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_username ON followers (username)")
        self.conn.commit()
    
    def add_follower(self, username):
        try:
            self.conn.execute("INSERT INTO followers (username) VALUES (?)", (username,))
            self.conn.commit()
            self.logger.info(f"`@{username}` successfully added to follower list.")
            return True # successfully added
        except sqlite3.IntegrityError:
            self.logger.error(f"Could not add `@{username}` to follower list, user is already following.")
            return False # already exists
    
    def check_follower(self, username):
        result = self.conn.execute("SELECT 1 FROM followers WHERE username = ?", (username,)).fetchone()
        return result is not None
    
    def close(self):
        self.conn.close()