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
        The passed feel from 0-10

    timestamp : `str`\n
        timestamp of the recorded feel

    """
    
    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO Feelings (Feel, Timestamp) VALUES ('{feel}', '{timestamp}')")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)

def setMeal(name: str):
    """
    Sets a meal into the db

    Parameters
    ----------
    name : `int`\n
        Name of the meal

    """
    
    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO Meals (Name) VALUES ('{name}'')")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)

def setIngredient(name: str):
    """
    Sets an ingredient entry into the db

    Parameters
    ----------
    name : `str`\n
        Name of the ingredient
    """
    
    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO Ingredients (Name) VALUES ('{name}')")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)
        
def setMealEntry(mealID: int, timestamp: str):
    """
    Sets a Meal Entry into the db

    Parameters
    ----------
    mealID : `int`\n
        ID of the meal
    timestamp : `str`\n
        time the meal was eaten
    """
    
    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO MealEntry (MealID, Timestamp) VALUES ('{mealID}', '{timestamp}')")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)

# --------------------------- JOIN TABLE FUNCTIONS ------------------------------- #
# -------------------------------------------------------------------------------- #
def setMealEntry_Ingredients(mealEntryID: int, ingredientID: int):
    """
    Sets an entry in the Join table of 2 named tables

    Parameters
    ----------
    mealEntryID : `int`\n
        ID of the Meal Entry
    ingredientID : `int`\n
        ID of the ingredient
    """
    
    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO MealEntry_Ingredients (EntryID, IngredientID) VALUES ('{mealEntryID}', '{ingredientID}')")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)

def setBase_Ingredients(mealID: int, ingredientID: int):
    """
    Sets an entry in the Join table of 2 named tables

    Parameters
    ----------
    mealID : `int`\n
        ID of the meal 
    ingredientID : `int`\n
        ID of the ingredient
    """
    
    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO Base_Ingredients (MealID, IngredientID) VALUES ('{mealID}', '{ingredientID}')")
        except sqlite3.Error as e:
            raise sqlite3.Error(e)

