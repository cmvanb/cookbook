function RecipeControls({ recipe }) {
    const editRecipe = () => console.error('editRecipe not implemented');

    const deleteRecipe = () => console.error('deleteRecipe not implemented');

    const exportRecipe = () => console.error('exportRecipe not implemented');

    return (
        <section id='recipe-controls' class='content'>
            <nav class='no-space'>
                <button class='border fill left-round' onClick={editRecipe}>
                    <i>edit</i>
                    <span>Edit</span>
                </button>
                <button class='border fill no-round' onClick={deleteRecipe}>
                    <i>delete</i>
                    <span>Delete</span>
                </button>
                <button class='border fill right-round' onClick={exportRecipe}>
                    <i>download</i>
                    <span>Export</span>
                </button>
            </nav>
        </section>
    );
}

export default RecipeControls
