/*------------------------------------------------------------------------------
    Entry point for the frontend application.
------------------------------------------------------------------------------*/
// @refresh reload

import { render } from 'solid-js/web';
import { Router, Route } from '@solidjs/router';

// Local styles will override global styles.
import 'beercss';
import './index.css';

import App from './App';
import Splash from './pages/Splash';
import NotFound from './pages/NotFound';
import Recipe from './pages/Recipe';
import Login from './pages/Login';
import Recipes from './pages/Recipes';
import MealPlanner from './pages/MealPlanner';
import Settings from './pages/Settings';

const root = document.getElementById('root');

if (import.meta.env.DEV && !(root instanceof HTMLElement)) {
    throw new Error(
        'Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?',
    );
}

render(
    () => (
        <Router root={App}>
            <Route path="/mealplanner" component={MealPlanner} />
            <Route path="/recipes" component={Recipes} />
            <Route path="/recipes/:id" component={Recipe} />
            <Route path="/settings" component={Settings} />
            <Route path="/login" component={Login} />
            <Route path="/" component={Splash} />
            <Route path="*" component={NotFound} />
        </Router>
    ),
    root);
