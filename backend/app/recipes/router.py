from fastapi import APIRouter, HTTPException

from app.auth.utils import CurrentUserDep
from app.core.db import SessionDep
from app.recipes.db import create_recipe, read_recipe, update_recipe, delete_recipe
from app.recipes.models import RecipeBase, RecipePublic


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
