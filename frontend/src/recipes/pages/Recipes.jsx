import { createResource, createSignal, Switch, Match } from 'solid-js'

import Page from '@/core/pages/Page'
import RecipeCard from '@/recipes/components/RecipeCard'
import RecipeService from '@/recipes/service'

import '@/recipes/pages/Recipes.css'


function Recipes() {
    // TODO: Implement search filter.
    const [searchFilter, setSearchFilter] = createSignal('')

    const [recipes] = createResource(
        async () => {
            await new Promise((resolve) => setTimeout(resolve, 200))
            const response = await RecipeService.getRecipes()
            return response.data
        })

    return (
        <Page>
            <div class='field large prefix round fill active'>
                <i class='front'>search</i>
                <input />
                <menu class='min'>
                    <div class='field large prefix suffix no-margin fixed'>
                        <i class='front'>arrow_back</i>
                        <input
                            placeholder='Search'
                            onInput={(e) => setSearchFilter(e.target.value)}
                        />
                        <i class='front'>close</i>
                    </div>
                </menu>
            </div>
            <Switch>
                <Match when={recipes.loading}>
                    <p>Loading...</p>
                </Match>
                <Match when={recipes.error}>
                    <p>Error: {recipes.error.message}</p>
                </Match>
                <Match when={recipes()}>
                    <div class='grid'>
                        {recipes().map((recipe) => (
                            <RecipeCard recipe={recipe}/>
                        ))}
                    </div>
                </Match>
            </Switch>
        </Page>
    )
}

export default Recipes
