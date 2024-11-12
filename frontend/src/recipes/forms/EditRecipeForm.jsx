import { createForm } from '@felte/solid'
import { reporter } from '@felte/reporter-solid'
import { createSignal, For } from 'solid-js'
import { useNavigate } from '@solidjs/router'
import { createFileUploader } from '@solid-primitives/upload'

import { ErrorCard, FormField } from '@/core/components'
import { isNumberWithValue, isStringWithValue } from '@/core/utils'
import { constants as vc, validate_all } from '@/core/validation'
import RecipeService from '@/recipes/service'
import DragAndDropListInput from '../components/DragAndDropListInput'

function EditRecipeForm({ recipe }) {
    const navigate = useNavigate()

    const [serverError, setServerError] = createSignal({
        message: null,
        renderHelp: null,
        detail: null,
    })
    const [ingredients, setIngredients] = createSignal(
        recipe.ingredients.map((ingredient, index) => ({
            id: index,
            text: ingredient.text,
        }))
    )
    const [instructions, setInstructions] = createSignal(
        recipe.instructions.map((instruction, index) => ({
            id: index,
            text: instruction.text,
        }))
    )

    const { files, selectFiles } = createFileUploader()

    const handleSubmit = async (data) => {
        data = {
            file: files().length > 0 ? files()[0].file : null,
            ingredients:  ingredients().map(
                (ingredient) => ({
                    text: ingredient.text,
                })),
            instructions: instructions().map(
                (instruction) => ({
                    text: instruction.text,
                })),
            ...data,
        }

        const response = await RecipeService.updateRecipe(recipe.id, data)

        setServerError({ message: null, renderHelp: null, detail: null })
        navigate(`/recipes/${response.id}`)
    }

    const handleError = (error) => {
        // NOTE: Needed for reactivity.
        setServerError({ message: null, renderHelp: null, detail: null })

        switch (error.status) {
            default:
                setServerError({
                    message: `Server error ${error.status}: ${error.statusText}`,
                    detail: error.body.detail,
                })
                break
        }
    }

    const { form, errors } = createForm({
        initialValues: {
            title: recipe.title,
            author: recipe.author,
            description: recipe.description,
            source_url: recipe.source_url,
            servings: recipe.servings,
            prep_time: recipe.prep_time,
            cook_time: recipe.cook_time,
            is_public: recipe.is_public
        },
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
            // TODO: URL must have a TLD.
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
        <form use:form>
            {serverError().message !== null && (
                <ErrorCard
                    message={serverError().message}
                    detail={serverError().detail}
                    renderHelp={serverError().renderHelp}
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
            <DragAndDropListInput
                id='ingredients'
                type='ingredients'
                label='Ingredients'
                items={ingredients}
                setItems={setIngredients}
            />
            <DragAndDropListInput
                id='instructions'
                type='instructions'
                label='Instructions'
                items={instructions}
                setItems={setInstructions}
            />
            <div class='field'>
                <button
                    class='file-upload-button'
                    type='button'
                    onClick={() => {
                        selectFiles(([{ source, name, size, file }]) => {
                            // TODO: Local validation.
                            console.log('Selected file:', { source, name, size, file })
                        })
                    }}
                >
                    <i>Upload</i>
                    <span>Upload image</span>
                </button>
                <For each={files()}>{(file) => {
                    return <span class='file-upload-text'>{file.name}</span>
                }}</For>
            </div>
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
    )
}

export default EditRecipeForm
