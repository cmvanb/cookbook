import { createSignal } from 'solid-js';

import TopBar from './components/TopBar';
import DrawerMenu from './components/DrawerMenu';
import { RecipeProvider } from './contexts/RecipeContext';

function App(props) {
    const [menuOpen, setMenuOpen] = createSignal(false);

    return (
        <RecipeProvider>
            <header>
                <TopBar menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
                <DrawerMenu menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
            </header>
            <main class="responsive">
                {props.children}
            </main>
            <footer>
            </footer>
        </RecipeProvider>
    );
}

export default App;
