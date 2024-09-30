function TopBar(props) {
    const toggleMenu = () => {
        props.setMenuOpen(!props.menuOpen());
    };

    return (
        <nav>
            <button class="circle transparent" onClick={toggleMenu}>
                <i>menu</i>
            </button>
            <h5 class="max center-align">Cookbook</h5>
        </nav>
    );
}

export default TopBar;
