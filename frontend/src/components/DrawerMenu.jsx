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
                <a href="/mealplanner">
                    <i>calendar_month</i>
                    <span>Meal Planner</span>
                </a>
                <a href="/recipes">
                    <i>menu_book</i>
                    <span>Recipes</span>
                </a>
                <hr class="medium" />
                <a href="/settings">
                    <i>settings</i>
                    <span>Settings</span>
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
