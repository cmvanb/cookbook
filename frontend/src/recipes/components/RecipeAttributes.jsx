function RecipeAttributes({ recipe }) {
    return (
        <section id='recipe-attributes' class='content'>
            <div class='middle-align recipe-attr'>
                <i class='small'>schedule</i>
                <span>Prep: {recipe.prep_time} mins</span>
            </div>
            <div class='middle-align recipe-attr'>
                <i class='small'>schedule</i>
                <span>Cook: {recipe.cook_time} mins</span>
            </div>
            <div class='middle-align recipe-attr'>
                <i class='small'>group</i>
                <span>Serves: {recipe.servings}</span>
            </div>
        </section>
    )
}

export default RecipeAttributes
