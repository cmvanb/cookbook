window.onload = () => {
    console.log('hello world');

    let modal_menu = document.getElementById('modal_menu');
    let modal_menu_button = document.getElementById('modal_menu_button');
    let close_modal_menu_button = document.getElementById('close_modal_menu_button');

    modal_menu_button.onclick = () => {
        modal_menu.classList.toggle('active');
    }

    close_modal_menu_button.onclick = () => {
        modal_menu.classList.remove('active');
    }
}
