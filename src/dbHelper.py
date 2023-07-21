import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_MEAL_ID_IDX=0
DB_MEAL_NAME_IDX=1
DB_INGREDIENT_ID_IDX=0
DB_INGREDIENT_NAME_IDX=1


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
    
    Returns
    ----------
    rowid : `int`\n
        id of the inserted feel

    """

    with SQLite() as cur:
        try:
            cur.execute(
                f"INSERT INTO Feelings (Feel, Timestamp) VALUES ('{feel}', '{timestamp}')"
            )
            return cur.lastrowid
        except sqlite3.Error as e:
            raise sqlite3.Error(e)


def setMeal(name: str):
    """
    Sets a meal into the db

    Parameters
    ----------
    name : `str`\n
        Name of the meal
    
    Returns
    ----------
    rowid : `int`\n
        id of the inserted meal

    """

    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO Meals (Name) VALUES ('{name}')")
            return cur.lastrowid
        except sqlite3.Error as e:
            raise sqlite3.Error(e)


def getMeal(name: str = "", id: int = 0):
    """
    Gets a meal from the db either by name or by unique id

    Parameters
    ----------
    name : `str`\n
        Name of the meal
    id   : `int`\n
        Unique ID of the meal

    Returns
    ----------
    meal : `tuple`\n
        Found meal
    """
    rows = None

    # First validate the input and determine how we retrieve the meal
    if name == "" and id == 0:
        return
    if id != 0:
        query = f"SELECT * FROM Meals WHERE MealID='{id}'"
        sqlParameter = id
    else:
        query = f"SELECT * FROM Meals WHERE Name='{name}'"
        sqlParameter = name

    with SQLite() as cur:
        try:
            cur.execute(query)
            rows = cur.fetchone()
            if rows is None:
                raise NotFoundError(f"Unable to find Meal: {sqlParameter}")

            return rows[0]

        except sqlite3.Error as e:
            raise sqlite3.Error(e)

def getAllMeals():
    """
    Gets all meals from the DB

    Returns
    ----------
        List of tuples with Meals : `List`
    """

    with SQLite() as cur:
        try:
            cur.execute("SELECT * FROM Meals;")
            return cur.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.Error(e)
        
    
def getMealIngredients(id: int):
    """
    Gets a base ingredients of a registered meal

    Parameters
    ----------
    id   : `int`\n
        Unique ID of the meal

    Returns
    ----------
    Ingredients : `tuple`\n
        Ingredients of the found meal
    """
    sqlQuery = f"SELECT Name FROM Ingredients"\
                "INNER JOIN Base_Ingredients ON Ingredients.IngredientID = Base_Ingredients.IngredientID"\
                "INNER JOIN Meals ON Meals.MealID = Base_Ingredients.MealID"\
                "WHERE MealID = '{id}';"
    with SQLite() as cur:
        try:
            cur.execute(sqlQuery)
            return cur.fetchall()
        except sqlite3.Error as e:
            raise sqlite3.Error(e)


def setIngredient(name: str):
    """
    Sets an ingredient entry into the db

    Parameters
    ----------
    name : `str`\n
        Name of the ingredient

    Returns
    ----------
    rowid : `int`\n
        id of the inserted ingredient
    """

    with SQLite() as cur:
        try:
            cur.execute(f"INSERT INTO Ingredients (Name) VALUES ('{name}')")
            return cur.lastrowid
        except sqlite3.Error as e:
            raise sqlite3.Error(e)


def getIngredient(name: str = "", id: int = 0):
    """
    Gets a ingredient from the db either by name or by unique id

    Parameters
    ----------
    name : `str`\n
        Name of the ingredient
    id   : `int`\n
        Unique ID of the ingredient

    Returns
    ----------
    ingredient : `tuple`\n
        Found ingredient
    """
    rows = None

    # First validate the input and determine how we retrieve the ingredient
    if name == "" and id == 0:
        return
    if id != 0:
        query = f"SELECT * FROM Ingredients WHERE IngredientID='{id}'"
        sqlParameter = id
    else:
        query = f"SELECT * FROM Ingredients WHERE Name='{name}'"
        sqlParameter = name

    with SQLite() as cur:
        try:
            cur.execute(query)
            rows = cur.fetchone()
            if rows is None:
                raise NotFoundError(f"Unable to find Ingredients: {sqlParameter}")

            return rows[0]

        except sqlite3.Error as e:
            raise sqlite3.Error(e)


def getAllIngredients():
    """
    Gets all Ingredients from the DB

    Returns
    ----------
        List of tuples with Ingredients : `List`
    """

    with SQLite() as cur:
        try:
            cur.execute("SELECT * FROM Ingredients;")
            return cur.fetchall()
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

    Returns
    ----------
    rowid : `int`\n
        id of the inserted MealEntry
    """

    with SQLite() as cur:
        try:
            cur.execute(
                f"INSERT INTO MealEntry (MealID, Timestamp) VALUES ('{mealID}', '{timestamp}')"
            )
            return cur.lastrowid
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
            cur.execute(
                f"INSERT INTO MealEntry_Ingredients (EntryID, IngredientID) VALUES ('{mealEntryID}', '{ingredientID}')"
            )
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
            cur.execute(
                f"INSERT INTO Base_Ingredients (MealID, IngredientID) VALUES ('{mealID}', '{ingredientID}')"
            )
        except sqlite3.Error as e:
            raise sqlite3.Error(e)
