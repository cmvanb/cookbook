import { useParams } from '@solidjs/router'

import { useRecipeContext } from '../context'

import './Recipe.css'

function Recipe() {
    const { recipeStore } = useRecipeContext()
    const params = useParams()
    const recipe = recipeStore.recipes[params.id]

    return (
        <article class='medium-elevate no-padding'>
            <img class='responsive' id='recipe-image' src='https://www.teaforturmeric.com/wp-content/uploads/2018/06/Chicken-Korma-in-pan.jpg' />
            <nav id='recipe-close-button'>
                <button class='transparent circle extra' onClick={() => location.href='/recipes'}>
                    <i>close</i>
                </button>
            </nav>
            <div class='padding'>
                <section class='header center-align'>
                    <h4>{recipe.title}</h4>
                    <p>by {recipe.author}</p>
                    <a class='link' href={recipe.source_url}>{recipe.source_url}</a>
                </section>
                <section id='recipe-attributes' class='content'>
                    <div class='middle-align recipe-attr'>
                        <i class='small'>schedule</i>
                        <span>Prep: {recipe.prep_time} mins</span>
                    </div>
                    <div class='middle-align recipe-attr'>
                        <i class='small'>schedule</i>
                        <span>Cook: {recipe.cook_time} mins</span>
                    </div>
                    <div class='middle-align recipe-attr'>
                        <i class='small'>group</i>
                        <span>Serves: {recipe.servings}</span>
                    </div>
                </section>
                <section class='content center-align'>
                    <p>{recipe.description}</p>
                </section>
                <section id='recipe-controls' class='content'>
                    <nav class='no-space'>
                        <button class='border fill left-round' onClick={() => console.warn('edit')}>
                            <i>edit</i>
                            <span>Edit</span>
                        </button>
                        <button class='border fill no-round' onClick={() => console.warn('delete')}>
                            <i>delete</i>
                            <span>Delete</span>
                        </button>
                        <button class='border fill right-round' onClick={() => console.warn('export')}>
                            <i>download</i>
                            <span>Export</span>
                        </button>
                    </nav>
                </section>
                <div>
                    <hr class='large' />
                </div>
                <section id='recipe-columns' class='content grid'>
                    <div class='s12 m6 recipe-col'>
                        <h6>Ingredients</h6>
                        <table class='border fill'>
                            <tbody>
                                {recipe.ingredients.map((ingredient) => (
                                    <tr>
                                        <td>{ingredient}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <div class='s12 m6 recipe-col'>
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
    )
}

export default Recipe
