window.onload = () => {
    let modal_menu = document.getElementById('modal-menu');

    console.assert(modal_menu);

    let modal_menu_button = document.getElementById('modal-menu-button');
    if (modal_menu_button) {
        modal_menu_button.onclick = () => {
            modal_menu.classList.toggle('active');
        }
    }

    let close_modal_menu_button = document.getElementById('close-modal-menu-button');
    if (close_modal_menu_button) {
        close_modal_menu_button.onclick = () => {
            modal_menu.classList.remove('active');
        }
    }

    let image_zoom = document.getElementById('view-recipe-image');
    if (image_zoom) {
        image_zoom.onclick = () => {
            modal_image_zoom.classList.toggle('active');
        }
    }

    let modal_image_zoom = document.getElementById('modal-image-zoom')
    if (modal_image_zoom) {
        // Close modal by clicking anywhere...
        modal_image_zoom.onclick = () => {
            modal_image_zoom.classList.remove('active');
        }
        // Or use the close button.
        let modal_image_zoom_close_button = document.getElementById('modal-image-zoom-close-button');
        modal_image_zoom_close_button.onclick = () => {
            modal_image_zoom.classList.remove('active');
        }
    }
}
