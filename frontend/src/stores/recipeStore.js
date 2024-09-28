import { createStore } from 'solid-js/store';

import { chicken_korma } from './mockData';

const [ recipeStore, setRecipeStore ] = createStore({
    recipes: [...Array(12).keys()].map((id) => ({ ...chicken_korma, id: id + 1 }) ),
});

export { recipeStore, setRecipeStore };
