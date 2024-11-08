from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import parse_pydantic_schema
from app.recipes.models import DbRecipe, RecipeBase


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


def read_recipes(*,
    session: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 24,
) -> list[DbRecipe]:
    """ Read a list of recipes. """

    recipes = list(session.execute(
        select(DbRecipe)
            .where(DbRecipe.owner_id == user_id)
            .offset(skip)
            .limit(limit)
    ).scalars().all())

    return recipes


def read_recipe(*,
    session: Session,
    recipe_id: int,
    user_id: int,
) -> DbRecipe | None:
    """ Read a single recipe. """

    recipe = session.execute(
        select(DbRecipe)
            .where(DbRecipe.owner_id == user_id)
            .where(DbRecipe.id == recipe_id)
    ).scalar_one_or_none()

    return recipe


def read_public_recipes(*,
    session: Session,
    skip: int = 0,
    limit: int = 24,
) -> list[DbRecipe]:
    """ Read a list of public recipes. """

    recipes = list(session.execute(
        select(DbRecipe)
            .where(DbRecipe.is_public == True)
            .offset(skip)
            .limit(limit)
    ).scalars().all())

    return recipes


def read_public_recipe(*,
    session: Session,
    recipe_id: int,
) -> DbRecipe | None:
    """ Read a single public recipe. """

    recipe = session.execute(
        select(DbRecipe)
            .where(DbRecipe.is_public == True)
            .where(DbRecipe.id == recipe_id)
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
            .where(DbRecipe.owner_id == user_id)
            .where(DbRecipe.id == recipe_id)
    ).scalar_one_or_none()

    if recipe is None:
        raise KeyError('Recipe not found')

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
            .where(DbRecipe.owner_id == user_id)
            .where(DbRecipe.id == recipe_id)
    ).scalar_one_or_none()

    if recipe is None:
        raise KeyError('Recipe not found')

    session.delete(recipe)
    session.commit()


def count_recipes(*,
    session: Session,
    user_id: int,
) -> int:
    """ Count a users recipes. """

    count = session.query(DbRecipe).filter(DbRecipe.owner_id == user_id).count()

    return count


def count_public_recipes(*,
    session: Session,
) -> int:
    """ Count public recipes. """

    count = session.query(DbRecipe).filter(DbRecipe.is_public == True).count()

    return count
