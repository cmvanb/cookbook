import { createResource, Switch, Match } from 'solid-js'
import { useParams } from '@solidjs/router'

import { Page } from '@/core/components'
import { RecipeAttributes, RecipeColumns, RecipeControls, RecipeHeader } from '@/recipes/components'
import RecipeService from '@/recipes/service'

import '@/recipes/pages/Recipe.css'


function Recipe() {
    const params = useParams()

    const [recipe] = createResource(
        async () => {
            await new Promise((resolve) => setTimeout(resolve, 500))
            const response = await RecipeService.getRecipe(params.id)
            return response
        })

    return (
        <Page>
            <Switch>
                <Match when={recipe.loading}>
                    <div>
                        <progress class='circle large center'></progress>
                    </div>
                </Match>
                <Match when={recipe.error}>
                    <p>Error: {recipe.error.message}</p>
                </Match>
                <Match when={recipe()}>
                    <article class='medium-elevate no-padding'>
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
                    </article>
                </Match>
            </Switch>
        </Page>
    )
}

export default Recipe
