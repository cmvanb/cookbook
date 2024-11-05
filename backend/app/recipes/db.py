from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.core.models import parse_pydantic_schema
from app.recipes.models import DbRecipe, RecipeBase, RecipeCreate


def create_recipe(*,
    session: Session,
    user_id: int,
    params: RecipeBase,
) -> DbRecipe:
    """ Create a new recipe. """

    schema = parse_pydantic_schema(params)
    recipe = DbRecipe(**schema, owner_id=user_id)

    session.add(recipe)
    session.commit()
    session.refresh(recipe)

    return recipe


def read_recipe(*,
    session: Session,
    recipe_id: int,
    user_id: int,
) -> DbRecipe | None:
    """ Read a single recipe. """

    recipe = session.execute(
        select(DbRecipe)
            .where(DbRecipe.id == recipe_id)
            .where(DbRecipe.owner_id == user_id)
    ).scalar_one_or_none()

    return recipe


def update_recipe(*,
    session: Session,
    recipe_id: int,
    user_id: int,
    params: RecipeBase,
) -> DbRecipe | None:
    """ Update an eisting recipe. """

    recipe = session.execute(
        select(DbRecipe)
            .where(DbRecipe.id == recipe_id)
            .where(DbRecipe.owner_id == user_id)
    ).scalar_one_or_none()

    if recipe is None:
        return None

    schema = parse_pydantic_schema(params)

    for key, value in schema.items():
        setattr(recipe, key, value)

    session.add(recipe)
    session.commit()
    session.refresh(recipe)

    return recipe


def delete_recipe(*,
    session: Session,
    recipe_id: int,
    user_id: int,
):
    """ Delete an existing recipe. """

    recipe = session.execute(
        select(DbRecipe)
            .where(DbRecipe.id == recipe_id)
            .where(DbRecipe.owner_id == user_id)
    ).scalar_one_or_none()

    if recipe is None:
        raise KeyError('Recipe not found')

    session.delete(recipe)
    session.commit()
