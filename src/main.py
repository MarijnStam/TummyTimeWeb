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
    return set(i[db.INGREDIENT_NAME_IDX] for i in db.getMealIngredients(db.getMeal(name=mealName)[db.MEAL_ID_IDX]))


# Returns the names of all stored meals in a set
@app.get("/meals/")
async def get_meal_names() -> Set[str]:
    return set((i[db.MEAL_NAME_IDX] for i in db.getAllMeals()))


@app.put("/feel/")
async def feel_entry(feeling: Feel) -> Feel:
    db.setFeel(feeling.feel, feeling.timestamp)
    return feeling

@app.put("/new_meal/")
async def new_meal(food: Food) -> Food:
    try:
        mealID = db.setMeal(food.mealName)
    except db.NotUniqueError as e:
        print(e)
        return

    # Store all the ingredients and update the join table with ingredients for this meal
    for ingredient in food.ingredients:
        try:
            ingredientID = db.setIngredient(ingredient)
        except db.NotUniqueError as e:
            ingredientID = db.getIngredient(name=ingredient)[db.INGREDIENT_ID_IDX]
            print(e)
        finally:
            db.setBase_Ingredients(mealID, ingredientID)
            
    return food

@app.put("/meal_entry/")
async def meal_entry(entry: MealEntry) -> MealEntry:
    # First retrieve the information of the meal 
    mealID = db.getMeal(name=entry.Meal.mealName)[db.MEAL_ID_IDX]

    # Register the Meal Entry and retrieve ID
    mealEntryID = db.setMealEntry(mealID, entry.timestamp)

    # Retrieve the base ingredients for this meal and append the extra ingredients.
    baseIngredients = set(i[db.INGREDIENT_NAME_IDX] for i in db.getMealIngredients(mealID))
    ingredients = baseIngredients.union(entry.Meal.ingredients)
    
    for ingredient in ingredients:
        try:
            ingredientID = db.setIngredient(ingredient)
        except db.NotUniqueError as e:
            ingredientID = db.getIngredient(name=ingredient)[db.INGREDIENT_ID_IDX]
            print(e)
        finally:
            db.setMealEntry_Ingredients(mealEntryID, ingredientID)
            
    return entry
            
        
