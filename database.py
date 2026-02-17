import sqlite3
import os

class Database:
    def __init__(self, db_path='data/verifications.db'):
        """
        Initialize the database connection and ensure the directory exists.
        
        Args:
            db_path (str): Path to the SQLite database file.
        """
        # Create directory if it doesn't exist
        directory = os.path.dirname(db_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
            
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.init_db()
    
    def init_db(self):
        """
        Create the verifications table if it does not exist.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS verifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                verification_url TEXT,
                verification_id TEXT,
                status TEXT,
                result TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
        
    def add_verification(self, verification_url, verification_id, status, result):
        """
        Insert a new verification record into the database.
        
        Args:
            verification_url (str): The URL used for verification.
            verification_id (str): The ID of the verification.
            status (str): Current status of the verification.
            result (str): Result of the verification.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO verifications (verification_url, verification_id, status, result)
            VALUES (?, ?, ?, ?)
        ''', (verification_url, verification_id, status, result))
        self.conn.commit()
        
    def get_recent(self, limit=10):
        """
        Retrieve the most recent verification records.
        
        Args:
            limit (int): Maximum number of records to return.
            
        Returns:
            list: List of dictionaries representing the verification records.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, verification_url, verification_id, status, result, created_at
            FROM verifications
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
