import './Recipe.css';

function Recipe() {
    const recipe = {
        title: 'Chicken Korma',
        author: 'Izzah',
        description: 'Looking for a Chicken Korma recipe that’s the real deal? This one-pot chicken korma is made in the Pakistani and North Indian way but without the fuss. All the mind-blowing flavor of korma – yet ready in much less time. After making & testing this korma for years, I’ve perfected it to the point that I can confidently call it the BEST chicken korma.',
        source_url: 'https://www.teaforturmeric.com/authentic-chicken-korma/',
        servings: 6,
        prep_time: 15,
        cook_time: 45,
        ingredients: [
            '1/3 cup neutral oil',
            '2 tbsp ghee, or sub more oil',
            '2 (~500 g) large onions, sliced*',
            '2 lbs bone-in, cut up, skinless chicken (or sub chicken thighs), cleaned and excess skin removed',
            '2 bay leaves',
            '1 tsp cumin seeds',
            '1/8 tsp whole black peppercorns',
            '3 green cardamom pods',
            '5 whole cloves',
            '1 1-inch cinnamon stick',
            '8-10 cloves garlic, crushed',
            '1 inch piece ginger, crushed',
            '2 small tomatoes* (optional), quartered',
            '3/4 cup plain, whole-milk yogurt',
            '2 tsp coriander powder',
            '1 tsp cumin powder',
            '1 tsp red chili powder or to taste',
            '1/2 tsp turmeric powder',
            '1/2 tsp paprika powder or Kashmiri red chili powder, optional – for color',
            '2 1/8 tsp salt, or to taste depending on amount of chicken',
            '2-3 green chili peppers, chopped',
            '1-2 black cardamom pods (optional)',
            '1 piece whole mace, or sub pinch ground mace or cinnamon',
            '½ tsp garam masala',
            'pinch nutmeg powder',
            '1/2 tsp diluted kewra essence, or sub rose water',
            '1/4 cup cilantro leaves, chopped, optional – for garnish',
            '10-12 blanched almonds, for garnish',
        ],
        instructions: [
            'Heat a large, heavy-bottomed pan over high heat. Once hot, add the oil and onions and sauté the onions until they are golden brown (~20-25 minutes depending on quantity). Remove the onions from the pan and transfer them to a food processor. Add tomatoes (if using) and yogurt to the food processor and process until mostly smooth.',
            'In the same pan used to brown onions, heat ghee (or oil) and add the whole spices, garlic, and ginger. Sauté for 30 seconds or until the garlic and ginger begin to darken. Add the chicken and fry it until it changes color (~5 minutes).',
            'Add the yogurt mixture to chicken along with the ground spices, salt, and green chili peppers and sauté until the mixture comes to a light simmer (~2-3 minutes).',
            'Lower the heat to medium-low, cover, and allow it to cook for 15 minutes. Uncover and stir in the black cardamom (if using), mace, garam masala, and nutmeg powder. Cover and cook again for 10 minutes.',
            'Raise the heat to high. Add 1/2 to 3/4 cup of water (depending on how thin you\'d like the curry) and bring to a boil. Lower the heat and allow chicken to simmer for another 2-3 minutes. The oil will have risen to the top. Sprinkle the kewra essence and stir. Turn off the heat and garnish with cilantro and blanched almonds.',
        ],
    };

    const closeRecipe = () => {
        console.warn('Not implemented yet.')
    }

    return (
        <article class="medium-elevate no-padding">
            <nav id="recipe-controls">
                <h6 class="max"></h6>
                <button class="transparent circle extra" onClick={closeRecipe}>
                    <i>close</i>
                </button>
            </nav>
            <img class="responsive" id="recipe-image" src="https://www.teaforturmeric.com/wp-content/uploads/2018/06/Chicken-Korma-in-pan.jpg" />
            <div class="padding">
                <section class="header center-align">
                    <h4>{recipe.title}</h4>
                    <p>by {recipe.author}</p>
                    <a class="link" href={recipe.source_url}>{recipe.source_url}</a>
                </section>
                <section id="recipe-attributes" class="content">
                    <div class="middle-align recipe-attr">
                        <i class="small">schedule</i>
                        <span>Prep: {recipe.prep_time} mins</span>
                    </div>
                    <div class="middle-align recipe-attr">
                        <i class="small">schedule</i>
                        <span>Cook: {recipe.cook_time} mins</span>
                    </div>
                    <div class="middle-align recipe-attr">
                        <i class="small">group</i>
                        <span>Serves: {recipe.servings}</span>
                    </div>
                </section>
                <section class="content center-align">
                    <p>{recipe.description}</p>
                </section>
                <section id="recipe-columns" class="content grid">
                    <div class="s12 m6 recipe-col">
                        <h6>Ingredients</h6>
                        <table class="border fill">
                            <tbody>
                                {recipe.ingredients.map((ingredient) => (
                                    <tr>
                                        <td>{ingredient}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <div class="s12 m6 recipe-col">
                        <h6>Instructions</h6>
                        <ol>
                            {recipe.instructions.map((instruction) => (
                                <li>{instruction}</li>
                            ))}
                        </ol>
                    </div>
                </section>
            </div>
        </article>
    );
}

export default Recipe;
