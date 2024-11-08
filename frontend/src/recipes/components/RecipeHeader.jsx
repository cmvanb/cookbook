function RecipeHeader({ recipe }) {
    return (
        <section class='header center-align'>
            <h4>{recipe.title}</h4>
            <p>by {recipe.author}</p>
            <a class='link' href={recipe.source_url}>{recipe.source_url}</a>
        </section>
    );
}

export default RecipeHeader
