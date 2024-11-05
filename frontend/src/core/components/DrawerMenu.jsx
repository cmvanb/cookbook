import { useNavigate } from '@solidjs/router'

import AuthService from '@/auth/service.js'

function DrawerMenu(props) {
    const { menuOpen, setMenuOpen } = props

    const navigate = useNavigate()

    const closeMenu = () => {
        setMenuOpen(false)
    }

    const logout = () => {
        AuthService.logout()
        navigate('/login')
    }

    if (!AuthService.isLoggedIn()) {
        return (
            <dialog class='left no-padding' classList={{ active: menuOpen() }}>
                <nav class='drawer'>
                    <header>
                        <nav>
                            <h6 class='max'></h6>
                            <button class='transparent circle large' onClick={closeMenu}>
                                <i>close</i>
                            </button>
                        </nav>
                    </header>
                    <a href='/' onClick={closeMenu}>
                        <i>home</i>
                        <span>Home</span>
                    </a>
                    <hr class='medium' />
                    <a href='/login' onClick={closeMenu}>
                        <i>login</i>
                        <span>Login</span>
                    </a>
                    <a href='/register' onClick={closeMenu}>
                        <i>app_registration</i>
                        <span>Register</span>
                    </a>
                </nav>
            </dialog>
        )
    }

    return (
        <dialog class='left no-padding' classList={{ active: menuOpen() }}>
            <nav class='drawer'>
                <header>
                    <nav>
                        <h6 class='max'></h6>
                        <button class='transparent circle large' onClick={closeMenu}>
                            <i>close</i>
                        </button>
                    </nav>
                </header>
                {/* TODO: Implement meal planner
                <a href='/mealplanner' onClick={closeMenu}>
                    <i>calendar_month</i>
                    <span>Meal Planner</span>
                </a>
                */}
                <a href='/' onClick={closeMenu}>
                    <i>home</i>
                    <span>Home</span>
                </a>
                <a href='/recipes' onClick={closeMenu}>
                    <i>menu_book</i>
                    <span>My Recipes</span>
                </a>
                <hr class='medium' />
                <a href='/settings' onClick={closeMenu}>
                    <i>settings</i>
                    <span>Settings</span>
                </a>
                <a onClick={logout}>
                    <i>logout</i>
                    <span>Log out</span>
                </a>
            </nav>
        </dialog>
    )
}

export default DrawerMenu
