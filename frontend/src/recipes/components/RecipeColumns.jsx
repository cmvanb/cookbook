function RecipeColumns({ recipe }) {
    return (
        <section id='recipe-columns' class='content grid'>
            <div class='s12 m6 recipe-col'>
                <h6>Ingredients</h6>
                <table class='border fill'>
                    <tbody>
                        {recipe.ingredients.map((ingredient) => (
                            <tr>
                                <td>{ingredient.count}{ingredient.unit} {ingredient.text} {ingredient.comment && ((ingredient.comment))}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div class='s12 m6 recipe-col'>
                <h6>Instructions</h6>
                <ol>
                    {recipe.instructions.map((instruction) => (
                        <li>{instruction.text}</li>
                    ))}
                </ol>
            </div>
        </section>
    )
}

export default RecipeColumns
