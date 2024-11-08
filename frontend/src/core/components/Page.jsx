import { createSignal } from 'solid-js'

import { DrawerMenu, TopBar } from '@/core/components'

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
