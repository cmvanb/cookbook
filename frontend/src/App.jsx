import 'beercss';
import { createSignal } from 'solid-js';

import TopBar from './components/TopBar';
import DrawerMenu from './components/DrawerMenu';

function App() {
    const [menuOpen, setMenuOpen] = createSignal(false);

    return (
        <div>
            <header>
                <TopBar menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
                <DrawerMenu menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
            </header>
            <main class="responsive">
                <div class="grid">
                    <div class="s6">
                        <h3>Hello world!</h3>
                    </div>
                    <div class="s6">
                        <h3>Content goes here.</h3>
                    </div>
                </div>
            </main>
            <footer>
            </footer>
        </div>
    );
}

export default App;
