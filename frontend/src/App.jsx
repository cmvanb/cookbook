import 'beercss';
import { createSignal } from 'solid-js';

import TopBar from './components/TopBar';
import DrawerMenu from './components/DrawerMenu';

function App(props) {
    const [menuOpen, setMenuOpen] = createSignal(false);

    return (
        <div>
            <header>
                <TopBar menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
                <DrawerMenu menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
            </header>
            <main class="responsive">
                {props.children}
            </main>
            <footer>
            </footer>
        </div>
    );
}

export default App;
