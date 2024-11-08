import { createResource, createSignal, Switch, Match } from 'solid-js'
import { useNavigate } from '@solidjs/router'

import { Page } from '@/core/components'
import { RecipeCard } from '@/recipes/components'
import RecipeService from '@/recipes/service'

import '@/recipes/pages/Recipes.css'


function Recipes() {
    const navigate = useNavigate()

    // TODO: Implement search filter.
    const [searchFilter, setSearchFilter] = createSignal('')

    const [recipes] = createResource(
        async () => {
            await new Promise((resolve) => setTimeout(resolve, 500))
            const response = await RecipeService.getRecipes()
            return response.data
        })

    const addRecipe = () => {
        navigate('/recipes/new')
    }

    return (
        <Page>
            <Switch>
                <Match when={recipes.loading}>
                    <div>
                        <progress class='circle large center'></progress>
                    </div>
                </Match>
                <Match when={recipes.error}>
                    <p>Error: {recipes.error.message}</p>
                </Match>
                <Match when={recipes()}>
                    <div class='row'>
                        <div class='field large prefix round fill active flex-grow'>
                            <i class='front'>search</i>
                            <input
                                placeholder='Search'
                                onInput={(e) => setSearchFilter(e.currentTarget.value)}
                            />
                        </div>
                        <button class='circle extra' onClick={addRecipe}>
                            <i>add</i>
                        </button>
                    </div>
                    <div class='grid'>
                        {recipes().map((recipe) => (
                            <RecipeCard recipe={recipe} />
                        ))}
                    </div>
                </Match>
            </Switch>
        </Page>
    )
}

export default Recipes
