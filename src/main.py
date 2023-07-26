from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from typing import Set
from typing_extensions import Annotated

from .dbHelper import create_db, get_session
from .models import *

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db()

# Returns a single meal including base ingredients
@app.get("/meal/{meal_id}", response_model=MealRead)
async def get_meal(*, session: Session = Depends(get_session), meal_id : int):
    meal = session.get(Meal, meal_id)
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal

# Returns all meals (without their base ingredients)
@app.get("/meals/", response_model=List[MealReadAll])
async def get_meals(*, session: Session = Depends(get_session)):
    return session.exec(select(Meal)).all()

@app.put("/feel/", response_model=FeelRead)
async def feel_entry(*, session: Session = Depends(get_session), feeling: FeelCreate):
    db_feel = Feel.from_orm(feeling)
    session.add(db_feel)
    session.commit()
    session.refresh(db_feel)
    return db_feel

@app.put("/new_meal/", response_model=MealReadAll)
async def new_meal(*, session: Session = Depends(get_session), new_meal: MealCreate):
    db_meal = Meal.from_orm(new_meal)
    ingredients = [Ingredient(name=x.name) for x in new_meal.ingredients]

    #We need to check what ingredients already exist in our DB. 
    new_ingredients = [x for x in ingredients if session.exec(select(Ingredient).where(Ingredient.name == f"{x.name}")).one_or_none() is None]
    
    #TODO Check if meal is unique or reject request
    # We also have to manually patch in the join table i guess?
    
    setattr(db_meal, 'ingredients', new_ingredients)
    
    session.add(db_meal)

    session.commit()
    session.refresh(db_meal)
    return db_meal

@app.put("/meal_entry/", response_model=MealEntryRead)
async def meal_entry(*, session: Session = Depends(get_session), entry: MealEntryCreate):
    db_meal_entry = MealEntry.from_orm(entry)
    session.add(db_meal_entry)
    session.commit()
    session.refresh(db_meal_entry)
    return db_meal_entry      

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance