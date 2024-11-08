import { createResource, Switch, Match } from 'solid-js'
import { useParams } from '@solidjs/router'

import Page from '@/core/pages/Page'
import RecipeHeader from '@/recipes/components/RecipeHeader'
import RecipeAttributes from '@/recipes/components/RecipeAttributes'
import RecipeControls from '@/recipes/components/RecipeControls'
import RecipeColumns from '@/recipes/components/RecipeColumns'
import RecipeService from '@/recipes/service'

import '@/recipes/pages/Recipe.css'


function Recipe() {
    const params = useParams()

    const [recipe] = createResource(
        async () => {
            await new Promise((resolve) => setTimeout(resolve, 200))
            const response = await RecipeService.getRecipe(params.id)
            return response
        })

    return (
        <Page>
            <article class='medium-elevate no-padding'>
                <Switch>
                    <Match when={recipe.loading}>
                        <p>Loading...</p>
                    </Match>
                    <Match when={recipe.error}>
                        <p>Error: {recipe.error.message}</p>
                    </Match>
                    <Match when={recipe()}>
                        <img class='responsive' id='recipe-image' src='https://www.teaforturmeric.com/wp-content/uploads/2018/06/Chicken-Korma-in-pan.jpg' />
                        <nav id='recipe-close-button'>
                            <button class='transparent circle extra' onClick={() => location.href='/recipes'}>
                                <i>close</i>
                            </button>
                        </nav>
                        <div class='padding'>
                            <RecipeHeader recipe={recipe()} />
                            <RecipeAttributes recipe={recipe()} />
                            <section class='content center-align'>
                                <p>{recipe().description}</p>
                            </section>
                            <RecipeControls recipe={recipe()} />
                            <div>
                                <hr class='large' />
                            </div>
                            <RecipeColumns recipe={recipe()} />
                        </div>
                    </Match>
                </Switch>
            </article>
        </Page>
    )
}

export default Recipe
