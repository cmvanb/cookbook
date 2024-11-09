import { useNavigate } from '@solidjs/router';

import RecipeService from '@/recipes/service'

function RecipeControls({ recipe }) {
    const navigate = useNavigate();

    const editRecipe = () => console.error('editRecipe not implemented');

    const deleteRecipe = async () => {
        await RecipeService.deleteRecipe(recipe.id);

        navigate('/recipes');
    }

    const exportRecipe = () => console.error('exportRecipe not implemented')

    return (
        <section id='recipe-controls' class='content'>
            <nav class='no-space'>
                <button class='border fill left-round' onClick={editRecipe}>
                    <i>edit</i>
                    <span>Edit</span>
                </button>
                <button class='border fill no-round' onClick={deleteRecipe}>
                    <i>delete</i>
                    <span>Delete</span>
                </button>
                <button class='border fill right-round' onClick={exportRecipe}>
                    <i>download</i>
                    <span>Export</span>
                </button>
            </nav>
        </section>
    )
}

export default RecipeControls
