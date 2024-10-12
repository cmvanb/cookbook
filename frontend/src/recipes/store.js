import { createStore } from 'solid-js/store'

import { chicken_korma } from './mockData'

const initialState = {
    // That's a lot of korma!
    recipes: [...Array(12).keys()]
        .map((index) => ({ ...chicken_korma, id: index + 1 }))
        .reduce((acc, e) => ({
            ...acc,
            [e['id']]: e,
        }), {}),
}

const [ recipeStore, setRecipeStore ] = createStore(initialState)

export { recipeStore, setRecipeStore }
