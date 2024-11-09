import { Page } from '@/core/components'
import { AddRecipeForm } from '@/recipes/forms'

function AddRecipe() {
    return (
        <Page>
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
                    <h4>Add new recipe</h4>
                </section>
                <section>
                    <AddRecipeForm />
                </section>
            </article>
        </Page>
    )
}

export default AddRecipe
