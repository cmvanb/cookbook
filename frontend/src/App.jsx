import { Router, Route } from '@solidjs/router'

import { RouteGuard } from '@/auth/components'
import { Login } from '@/auth/pages'
import { NotFound, Settings, Splash } from '@/core/pages'
import { Recipes, AddRecipe, ViewRecipe } from '@/recipes/pages'
import { Register } from '@/users/pages'

function App() {
    return (
        <Router>
            <Route path='/login' component={Login} />
            <Route path='/register' component={Register} />
            <Route path='/' component={Splash} />
            <Route path='/' component={RouteGuard}>
                <Route path='/settings' component={Settings} />
                <Route path='/recipes' component={Recipes} />
                <Route path='/recipes/:id' component={ViewRecipe} />
                <Route path='/recipes/new' component={AddRecipe} />
            </Route>
            <Route path='*' component={NotFound} />
        </Router>
    )
}

export default App
