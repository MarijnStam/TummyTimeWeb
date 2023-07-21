from fastapi import FastAPI, Body, Request
from pydantic import BaseModel

from typing import Set
from typing_extensions import Annotated

import src.dbHelper as db


class Feel(BaseModel):
    feel: Annotated[int, Body(gt=0, le=10)]
    timestamp: str


class Food(BaseModel):
    ingredients: Set[str] = set()
    mealName: str

class MealEntry(BaseModel):
    Meal: Food
    timestamp: str


app = FastAPI()

# Returns the base ingredients for a meal
@app.get("/meal_ingredients/")
async def get_ingredients(mealName : str) -> Set[str]:
    meal = db.getMeal(name=mealName)
    return set(db.getMealIngredients(meal[db.DB_MEAL_ID_IDX]))

# Returns the names of all stored meals in a set
@app.get("/meals/")
async def get_meal_names() -> Set[str]:
    meals = set()
    dbResult = db.getAllMeals()
    for meal in dbResult:
        meals.add(meal[db.DB_MEAL_NAME_IDX])

    return meals

@app.put("/feel/")
async def feel_entry(feeling: Feel):
    db.setFeel(feeling.feel, feeling.timestamp)
    return feeling

@app.put("/new_meal/")
async def new_meal(food: Food):
    #TODO Handle case where meal is already in db
    mealID = db.setMeal(food.mealName)

    # Store all the ingredients and update the join table with ingredients for this meal
    # TODO Handle case where ingredient is already in db
    for ingredient in food.ingredients:
        ingredientID = db.setIngredient(ingredient)
        db.setBase_Ingredients(mealID, ingredientID)

    return food

@app.put("/meal_entry/")
async def meal_entry(entry: MealEntry):
    # First retrieve the information of the meal 
    mealID = db.getMeal(name=entry.Meal.mealName)[db.DB_MEAL_ID_IDX]

    # Register the Meal Entry and retrieve
    mealEntryID = db.setMealEntry(mealID, entry.timestamp)

    # Retrieve the base ingredients for this meal and append the extra ingredients.
    # TODO Handle case where ingredient is already in db
    baseIngredients = set(db.getMealIngredients(mealID))
    for ingredient in entry.Meal.ingredients:
        baseIngredients.add(ingredient)
        ingredientID = db.setIngredient(ingredient)
        db.setMealEntry_Ingredients(mealEntryID, ingredientID)
