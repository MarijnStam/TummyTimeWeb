from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

    
# Join tables for setting up the many-to-many relations
class MealIngredient(SQLModel, table=True):
    meal_id: Optional[int] = Field(
        default=None, foreign_key="meal.id", primary_key=True
    )
    ingredient_id: Optional[int] = Field(
        default=None, foreign_key="ingredient.id", primary_key=True
    )
    
class MealEntryIngredients(SQLModel, table=True):
    meal_entry_id: Optional[int] = Field(
        default=None, foreign_key="mealentry.id", primary_key=True
    )
    ingredient_id: Optional[int] = Field(
        default=None, foreign_key="ingredient.id", primary_key=True
    )
    
# ------------ Ingredient Models -------------- #
# --------------------------------------------- #    
class IngredientBase(SQLModel):
    name: str = Field(index=True, unique=True)
    
class Ingredient(IngredientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    meals: List["Meal"] = Relationship(back_populates="ingredients", link_model=MealIngredient)
    meal_entries: List["MealEntry"] = Relationship(back_populates="ingredients", link_model=MealEntryIngredients)
    
class IngredientCreate(IngredientBase):
    pass

class IngredientRead(IngredientBase):
    id: int


# ------------- MealEntry Models -------------- #
# --------------------------------------------- #    
class MealEntryBase(SQLModel):
    timestamp: str
    meal_id: Optional[int] = Field(default=None, foreign_key="meal.id")

class MealEntry(MealEntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    meal: Optional["Meal"] = Relationship(back_populates="meal_entries")
    ingredients: List[Ingredient] = Relationship(back_populates="meal_entries", link_model=MealEntryIngredients)
    
class MealEntryCreate(MealEntryBase):
    ingredients: Optional[List[IngredientCreate]] = []

class MealEntryRead(MealEntryBase):
    id: int    
    
# ---------------- Meal Models ---------------- #
# --------------------------------------------- #
class MealBase(SQLModel):
    name: str = Field(index=True, unique=True)

class Meal(MealBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ingredients: List[Ingredient] = Relationship(back_populates="meals", link_model=MealIngredient)
    meal_entries: Optional[List[MealEntry]] = Relationship(back_populates="meal")
    
class MealCreate(MealBase):
    ingredients: List[IngredientCreate] = []

class MealReadAll(MealBase):
    id: int
    
class MealRead(MealBase):
    id: int
    ingredients: List[IngredientRead] = []
  
# --------------- Feel Models ----------------- #
# --------------------------------------------- # 
class FeelBase(SQLModel):
    timestamp: str
    feel: int
       
class Feel(FeelBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class FeelCreate(FeelBase):
    pass

class FeelRead(FeelBase):
    id: int
    
