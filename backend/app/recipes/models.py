from annotated_types import Len
from typing import Annotated, Optional
import json

from pydantic import BaseModel, Field, ConfigDict, model_validator
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
    is_public: Mapped[bool] = mapped_column(Boolean)
    image_url: Mapped[Optional[str]] = mapped_column(String(255))


# Transport layer
#-------------------------------------------------------------------------------

# Requests
class Ingredient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    class Meta:
        orm_model = DbIngredient

    text: Annotated[str, Field(max_length=255)]

class Instruction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    class Meta:
        orm_model = DbInstruction

    text: Annotated[str, Field(max_length=4000)]

class RecipeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    class Meta:
        orm_model = DbRecipe

    # NOTE: Necessary to process form data as JSON.
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    ingredients: Annotated[list[Ingredient], Len(min_length=1)]
    instructions: Annotated[list[Instruction], Len(min_length=1)]
    title: Annotated[str, Field(max_length=255)]
    author: Annotated[str, Field(max_length=255)]
    description: Annotated[str, Field(max_length=4000)]
    source_url: Annotated[str, Field(max_length=255)]
    servings: Annotated[int, Field(gt=0, lt=1000000000)]
    prep_time: Annotated[int, Field(gt=0, lt=1000000000)]
    cook_time: Annotated[int, Field(gt=0, lt=1000000000)]
    is_public: bool

# Responses
class RecipePublic(RecipeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    image_url: Annotated[Optional[str], Field(max_length=255)]

class RecipesPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: list[RecipePublic]
    count: int
