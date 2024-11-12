import { createResource, Switch, Match } from 'solid-js'
import { useParams } from '@solidjs/router'

import { Page } from '@/core/components'
import { EditRecipeForm } from '@/recipes/forms'
import RecipeService from '@/recipes/service'

function EditRecipe() {
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
                    <article>
                        <nav id='recipe-close-button'>
                            <button
                                class='transparent circle extra'
                                onClick={() => (location.href = '/recipes')}
                            >
                                <i>close</i>
                            </button>
                        </nav>
                        <section class='header center-align'>
                            <h4>Edit recipe</h4>
                        </section>
                        <section>
                            <EditRecipeForm recipe={recipe()} />
                        </section>
                    </article>
                </Match>
            </Switch>
        </Page>
    )
}

export default EditRecipe
