function DrawerMenu(props) {
    const closeMenu = () => {
        props.setMenuOpen(false);
    };

    return (
        <dialog class="left no-padding" classList={{ active: props.menuOpen() }}>
            <nav class="drawer">
                <header>
                    <nav>
                        <h6 class="max"></h6>
                        <button class="transparent circle large" onClick={closeMenu}>
                            <i>close</i>
                        </button>
                    </nav>
                </header>
                <a>
                    <i>calendar_month</i>
                    <span>Meal Planner</span>
                </a>
                <a>
                    <i>menu_book</i>
                    <span>Recipes</span>
                </a>
                <hr />
                <a>
                    <i>settings</i>
                    <span>Settings</span>
                </a>
                <a>
                    <i>account_circle</i>
                    <span>Account</span>
                </a>
                <a>
                    <i>logout</i>
                    <span>Log out</span>
                </a>
            </nav>
        </dialog>
    );
}

export default DrawerMenu;
