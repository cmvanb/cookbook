import './Recipe.css';

import { useRecipeContext } from '../../contexts/RecipeContext';

function Recipe() {
    const { recipeStore } = useRecipeContext();
    const recipe = recipeStore.recipes[0];

    return (
        <article class="medium-elevate no-padding">
            <nav id="recipe-controls">
                <h6 class="max"></h6>
                <button class="transparent circle extra" onClick={() => location.href='/recipes'}>
                    <i>close</i>
                </button>
            </nav>
            <img class="responsive" id="recipe-image" src="https://www.teaforturmeric.com/wp-content/uploads/2018/06/Chicken-Korma-in-pan.jpg" />
            <div class="padding">
                <section class="header center-align">
                    <h4>{recipe.title}</h4>
                    <p>by {recipe.author}</p>
                    <a class="link" href={recipe.source_url}>{recipe.source_url}</a>
                </section>
                <section id="recipe-attributes" class="content">
                    <div class="middle-align recipe-attr">
                        <i class="small">schedule</i>
                        <span>Prep: {recipe.prep_time} mins</span>
                    </div>
                    <div class="middle-align recipe-attr">
                        <i class="small">schedule</i>
                        <span>Cook: {recipe.cook_time} mins</span>
                    </div>
                    <div class="middle-align recipe-attr">
                        <i class="small">group</i>
                        <span>Serves: {recipe.servings}</span>
                    </div>
                </section>
                <section class="content center-align">
                    <p>{recipe.description}</p>
                </section>
                <section id="recipe-columns" class="content grid">
                    <div class="s12 m6 recipe-col">
                        <h6>Ingredients</h6>
                        <table class="border fill">
                            <tbody>
                                {recipe.ingredients.map((ingredient) => (
                                    <tr>
                                        <td>{ingredient}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <div class="s12 m6 recipe-col">
                        <h6>Instructions</h6>
                        <ol>
                            {recipe.instructions.map((instruction) => (
                                <li>{instruction}</li>
                            ))}
                        </ol>
                    </div>
                </section>
            </div>
        </article>
    );
}

export default Recipe;
