import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SQLite:
    """
    This class is a context manager for the database.
    Use this for handling db operations within this file
    """
    def __init__(self):
        self.dbName = os.path.join(BASE_DIR, "TummyTime.db")
    def __enter__(self):
        self.conn = sqlite3.connect(self.dbName)
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

class NotFoundError(Exception):
    pass

def setFeel(feel: int, timestamp: str):
    """
    Sets a feeling entry into the db

    Parameters
    ----------
    feel : `int`\n
        The postcount after increment

    timestamp : `str`\n
        Name of the user to increment postcount for

    """
    
    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO Feelings (Feel, Timestamp) VALUES ('{feel}', '{timestamp}')")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)
