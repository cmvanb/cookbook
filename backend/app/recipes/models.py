from typing import Annotated
from annotated_types import Len

from pydantic import BaseModel, Field
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import DbBase


# Database layer
#-------------------------------------------------------------------------------

class DbIngredient(DbBase):
    __tablename__ = 'ingredients'

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id'))
    recipe: Mapped['DbRecipe'] = relationship(back_populates='ingredients')

    text: Mapped[str] = mapped_column(String(255))
    count: Mapped[float]
    unit: Mapped[str] = mapped_column(String(255))
    comment: Mapped[str] = mapped_column(String(255))

class DbInstruction(DbBase):
    __tablename__ = 'instructions'

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id'))
    recipe: Mapped['DbRecipe'] = relationship(back_populates='instructions')

    text: Mapped[str] = mapped_column(String(4000))

class DbRecipe(DbBase):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    ingredients: Mapped[list['DbIngredient']] = relationship(
        back_populates='recipe',
        cascade="all, delete-orphan",
    )
    instructions: Mapped[list['DbInstruction']] = relationship(
        back_populates='recipe',
        cascade="all, delete-orphan",
    )
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(4000))
    source_url: Mapped[str] = mapped_column(String(255))
    servings: Mapped[int]
    prep_time: Mapped[int]
    cook_time: Mapped[int]
    image_url: Mapped[str] = mapped_column(String(255))
    is_public: Mapped[bool] = mapped_column(Boolean)


# Transport layer
#-------------------------------------------------------------------------------

# Requests
class Ingredient(BaseModel):
    class Meta:
        orm_model = DbIngredient

    text: Annotated[str, Field(max_length=255)]
    count: Annotated[float, Field(gt=0)]
    unit: Annotated[str, Field(max_length=255)]
    comment: Annotated[str, Field(max_length=255)]

class Instruction(BaseModel):
    class Meta:
        orm_model = DbInstruction

    text: Annotated[str, Field(max_length=4000)]

class RecipeBase(BaseModel):
    class Meta:
        orm_model = DbRecipe

    title: Annotated[str, Field(max_length=255)]
    author: Annotated[str, Field(max_length=255)]
    description: Annotated[str, Field(max_length=4000)]
    source_url: Annotated[str, Field(max_length=255)]
    servings: Annotated[int, Field(gt=0)]
    prep_time: Annotated[int, Field(gt=0)]
    cook_time: Annotated[int, Field(gt=0)]
    image_url: Annotated[str, Field(max_length=255)]
    ingredients: Annotated[list[Ingredient], Len(min_length=1)]
    instructions: Annotated[list[Instruction], Len(min_length=1)]
    is_public: bool

# Responses
class RecipePublic(RecipeBase):
    id: int
    owner_id: int

class RecipesPublic(BaseModel):
    data: list[RecipePublic]
    count: int
