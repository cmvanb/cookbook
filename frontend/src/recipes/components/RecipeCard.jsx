function RecipeCard({ recipe }) {
    return (
        <article class='recipe-card medium-elevate no-padding s12 m6 l4'>
            <a href={`/recipes/${recipe.id}`}>
                <img class='responsive small' src='https://www.teaforturmeric.com/wp-content/uploads/2018/06/Chicken-Korma-in-pan.jpg' />
                <div class='padding'>
                    <h6>{recipe.title}</h6>
                    <p>{recipe.description}</p>
                </div>
            </a>
        </article>
    );
}

export default RecipeCard
