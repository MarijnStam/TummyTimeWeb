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
    timestamp: str

app = FastAPI()


@app.get("/hello_world")
async def root():
    return {"message": "Hello World"}

@app.put("/feel/")
async def create_feel_entry(feeling: Feel):
    db.setFeel(feeling.feel, feeling.timestamp)
    return feeling

@app.put("/food/")
async def create_food_entry(food: Food):
    print(food.mealName)
    print(food.ingredients)
    return food