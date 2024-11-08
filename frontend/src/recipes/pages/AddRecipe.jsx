import { createForm } from '@felte/solid'
import { reporter } from '@felte/reporter-solid'
import { createSignal } from 'solid-js'
import { useNavigate } from '@solidjs/router'

import { ErrorCard, FormField, Page } from '@/core/components'
import { isNumberWithValue, isStringWithValue } from '@/core/utils'
import { constants as vc, validate_all } from '@/core/validation'
import RecipeService from '@/recipes/service'

function AddRecipe() {
    const navigate = useNavigate()

    const [validationError, setValidationError] = createSignal({
        message: null,
        renderHelp: null,
        details: null,
    })

    const handleSubmit = async (data) => {
        await RecipeService.createRecipe({ body: data })

        // TODO: Redirect to the new recipe page.
    }

    const handleError = (error) => {
        switch (error.status) {
            default:
                setValidationError({
                    message: `Server error ${error.status}: ${error.statusText}`,
                    details: error.body.detail,
                })
                break
        }
    }

    const { form, errors } = createForm({
        onSubmit: handleSubmit,
        onError: handleError,
        extend: [reporter],
        validate: (values) => {
            const errors = {}

            errors.title = validate_all(
                values.title,
                [(v) => !isStringWithValue(v),
                    'Title is required'],
                [(v) => v && v.length > vc.STRING_MAX,
                    `Title cannot exceed ${vc.STRING_MAX} characters`],
            )
            errors.author = validate_all(
                values.author,
                [(v) => !isStringWithValue(v),
                    'Author is required'],
                [(v) => v && v.length > vc.STRING_MAX,
                    `Author cannot exceed ${vc.STRING_MAX} characters`],
            )
            errors.description = validate_all(
                values.description,
                [(v) => !isStringWithValue(v),
                    'Description is required'],
                [(v) => v && v.length > vc.TEXT_MAX,
                    `Description cannot exceed ${vc.TEXT_MAX} characters`],
            )
            errors.source_url = validate_all(
                values.source_url,
                [(v) => (v && v.length > vc.STRING_MAX),
                    `Source URL cannot exceed ${vc.STRING_MAX} characters`],
                [(v) => v && !/https:\/\/.*/.test(v),
                    'Source URL must start with https://'],
            )
            errors.servings = validate_all(
                values.servings,
                [(v) => !isNumberWithValue(v),
                    'Servings is required'],
                [(v) => v <= 0,
                    'Servings must be greater than 0'],
                [(v) => v > vc.NUMBER_MAX,
                    'Servings cannot exceed 999999999'],
            )
            errors.prep_time = validate_all(
                values.prep_time,
                [(v) => !isNumberWithValue(v),
                    'Prep Time is required'],
                [(v) => v <= 0,
                    'Prep Time must be greater than 0'],
                [(v) => v > vc.NUMBER_MAX,
                    'Prep Time cannot exceed 999999999'],
            )
            errors.cook_time = validate_all(
                values.cook_time,
                [(v) => !isNumberWithValue(v),
                    'Cook Time is required'],
                [(v) => v <= 0,
                    'Cook Time must be greater than 0'],
                [(v) => v > vc.NUMBER_MAX,
                    'Cook Time cannot exceed 999999999'],
            )

            return errors
        },
    })

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
                    <form use:form>
                        {validationError().message !== null && (
                            <ErrorCard
                                message={validationError().message}
                                details={validationError().details}
                                renderHelp={validationError().renderHelp}
                            />
                        )}
                        <FormField
                            name='title'
                            type='text'
                            label='Title'
                            required
                            errors={errors}
                        />
                        <FormField
                            name='author'
                            type='text'
                            label='Author'
                            required
                            errors={errors}
                        />
                        <FormField
                            name='description'
                            type='text'
                            label='Description'
                            required
                            errors={errors}
                        />
                        <FormField
                            name='source_url'
                            type='url'
                            pattern='https://.*'
                            label='Source URL'
                            errors={errors}
                        />
                        <FormField
                            name='servings'
                            type='number'
                            label='Servings'
                            required
                            errors={errors}
                        />
                        <FormField
                            name='prep_time'
                            type='number'
                            label='Prep Time (minutes)'
                            required
                            errors={errors}
                        />
                        <FormField
                            name='cook_time'
                            type='number'
                            label='Cook Time (minutes)'
                            required
                            errors={errors}
                        />
                        <div class='field'>
                            <label class='checkbox'>
                                <input
                                    id='is_public'
                                    name='is_public'
                                    type='checkbox'
                                />
                                <span>Is Public</span>
                            </label>
                        </div>
                        <nav class='row'>
                            <button type='submit'>Save</button>
                        </nav>
                    </form>
                </section>
            </article>
        </Page>
    )
}

export default AddRecipe
