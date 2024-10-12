import { Router, Route } from '@solidjs/router'
import { MultiProvider } from '@solid-primitives/context'

import RouteGuard from '@/auth/components/RouteGuard'
import Login from '@/auth/pages/Login'
import NotFound from '@/core/pages/NotFound'
import Settings from '@/core/pages/Settings'
import Splash from '@/core/pages/Splash'
import { RecipeProvider } from '@/recipes/context'
import Recipe from '@/recipes/pages/Recipe'
import Recipes from '@/recipes/pages/Recipes'
import Register from '@/users/pages/Register'

function App() {
    return (
        <MultiProvider
            values={[
                RecipeProvider,
            ]}
        >
            <Router>
                <Route path='/login' component={Login} />
                <Route path='/register' component={Register} />
                <Route path='/' component={Splash} />
                <Route path='/' component={RouteGuard}>
                    <Route path='/settings' component={Settings} />
                    <Route path='/recipes' component={Recipes} />
                    <Route path='/recipes/:id' component={Recipe} />
                </Route>
                <Route path='*' component={NotFound} />
            </Router>
        </MultiProvider>
    )
}

export default App
