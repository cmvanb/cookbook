import { createContext, useContext } from 'solid-js';

import { recipeStore } from '../stores/recipeStore';

const RecipeContext = createContext();

function RecipeProvider(props) {
    return (
        <RecipeContext.Provider
            value={{
                recipeStore,
            }}
        >
            {props.children}
        </RecipeContext.Provider>
    );
}

function useRecipeContext() {
    return useContext(RecipeContext);
}

export { RecipeProvider, useRecipeContext };
