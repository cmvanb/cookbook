import { createSignal } from 'solid-js'

import TopBar from '@/core/components/TopBar'
import DrawerMenu from '@/core/components/DrawerMenu'

function Page(props) {
    const [menuOpen, setMenuOpen] = createSignal(false)

    return (
        <>
            <header>
                <TopBar menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
                <DrawerMenu menuOpen={menuOpen} setMenuOpen={setMenuOpen} />
            </header>
            <main class='responsive'>
                {props.children}
            </main>
            <footer>
                Disclaimer goes here.
            </footer>
        </>
    )
}

export default Page
