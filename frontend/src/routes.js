import Splash from './pages/Splash';
import Login from './pages/Login';
import Recipes from './pages/Recipes';
import Recipe from './pages/Recipe';
import MealPlanner from './pages/MealPlanner';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';

export const routes = [
    {
        path: '/',
        component: Splash,
    },
    {
        path: '/login',
        component: Login,
    },
    {
        path: '/recipes',
        component: Recipes,
    },
    {
        path: '/recipe/:id',
        component: Recipe,
    },
    {
        path: '/mealplanner',
        component: MealPlanner,
    },
    {
        path: '/settings',
        component: Settings,
    },
    {
        path: '**',
        component: NotFound,
    }
];
