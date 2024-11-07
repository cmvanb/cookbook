from fastapi import APIRouter, HTTPException

from app.auth.utils import CurrentUserDep
from app.core.db import SessionDep
from app.recipes.db import (
    create_recipe, read_recipes, read_recipe, read_public_recipes,
    read_public_recipe, update_recipe, delete_recipe, count_recipes,
    count_public_recipes,
)
from app.recipes.models import RecipeBase, RecipePublic, RecipesPublic


router = APIRouter()


@router.post('/create', response_model=RecipePublic)
def create(
    session: SessionDep,
    current_user: CurrentUserDep,
    body: RecipeBase,
):
    recipe = create_recipe(
        session=session,
        user_id=current_user.id,
        params=body,
    )

    return recipe


@router.get('/read/', response_model=RecipesPublic)
def read_list(
    session: SessionDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 24,
):
    recipes = read_recipes(
        session=session,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    count = count_recipes(
        session=session,
        user_id=current_user.id,
    )
    data = [RecipePublic.model_validate(recipe) for recipe in recipes]

    return RecipesPublic(data=data, count=count)


@router.get('/read/{recipe_id}', response_model=RecipePublic)
def read(
    session: SessionDep,
    current_user: CurrentUserDep,
    recipe_id: int,
):
    recipe = read_recipe(
        session=session,
        user_id=current_user.id,
        recipe_id=recipe_id,
    )

    if recipe is None:
        raise HTTPException(status_code=404, detail='Recipe not found')

    return recipe


@router.get('/read/public/', response_model=RecipesPublic)
def read_public_list(
    session: SessionDep,
    skip: int = 0,
    limit: int = 24,
):
    recipes = read_public_recipes(
        session=session,
        skip=skip,
        limit=limit,
    )
    count = count_public_recipes(
        session=session,
    )
    data = [RecipePublic.model_validate(recipe) for recipe in recipes]

    return RecipesPublic(data=data, count=count)


@router.get('/read/public/{recipe_id}', response_model=RecipePublic)
def read_public(
    session: SessionDep,
    recipe_id: int,
):
    recipe = read_public_recipe(
        session=session,
        recipe_id=recipe_id,
    )

    if recipe is None:
        raise HTTPException(status_code=404, detail='Recipe not found')

    return recipe


@router.put('/update/{recipe_id}', response_model=RecipePublic)
def update(
    session: SessionDep,
    current_user: CurrentUserDep,
    recipe_id: int,
    body: RecipeBase,
):
    recipe = update_recipe(
        session=session,
        user_id=current_user.id,
        recipe_id=recipe_id,
        params=body,
    )

    if recipe is None:
        raise HTTPException(status_code=404, detail='Recipe not found')

    return recipe


@router.delete('/delete/{recipe_id}')
def delete(
    session: SessionDep,
    current_user: CurrentUserDep,
    recipe_id: int,
):
    try:
        recipe = delete_recipe(
            session=session,
            recipe_id=recipe_id,
            user_id=current_user.id,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail='Recipe not found')

    return recipe
