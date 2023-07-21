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

app = FastAPI()

@app.get("/ingredients/")
#TODO Format to return only ingredient names and not IDs
async def get_ingredients() -> Set[str]:
    return db.getAllIngredients() 

@app.get("/meal_names/")
#TODO Format to return only ingredient names and not IDs
async def get_meal_names() -> Set[str]:
    return db.getAllMeals()

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
async def meal_entry(food: Food):
    return food



