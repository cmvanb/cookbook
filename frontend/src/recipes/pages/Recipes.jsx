import Page from '@/core/pages/Page'
import { useRecipeContext } from '@/recipes/context'
import '@/recipes/pages/Recipes.css'

function Recipes() {
    const { recipeStore } = useRecipeContext()
    const recipes = recipeStore.recipes

    return (
        <Page>
            <div class='field large prefix round fill active'>
                <i class='front'>search</i>
                <input />
                <menu class='min'>
                    <div class='field large prefix suffix no-margin fixed'>
                        <i class='front'>arrow_back</i>
                        <input />
                        <i class='front'>close</i>
                    </div>
                </menu>
            </div>
            <div class='grid'>
                <For each={Object.keys(recipes)}>
                    {(recipeId) => (
                        <article class='recipe-card medium-elevate no-padding s12 m6 l4'>
                            <a href={`/recipes/${recipeId}`}>
                                <img class='responsive small' src='https://www.teaforturmeric.com/wp-content/uploads/2018/06/Chicken-Korma-in-pan.jpg' />
                                <div class='padding'>
                                    <h6>{recipes[recipeId].title}</h6>
                                    <p>{recipes[recipeId].description}</p>
                                </div>
                            </a>
                        </article>
                    )}
                </For>
            </div>
        </Page>
    )
}

export default Recipes
