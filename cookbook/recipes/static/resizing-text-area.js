export class ResizingTextArea {
    static initialize() {
        let fields = Array.from(document.getElementsByClassName('textarea'));

        fields.forEach(
            (f) => new ResizingTextArea(f));
    }

    constructor(field) {
        this.field = field;

        this.textArea = this.field.getElementsByTagName('textarea')[0];

        this.updateSize();
        this.textArea.oninput = () => {
            this.updateSize();
        }
    }

    updateSize() {
        // NOTE: Weird looking hack, but it works. We need to force the browser
        // to recompute the height later.
        this.textArea.style.height = '0%';

        // 16 is the padding offset.
        let height = Math.max(this.textArea.offsetHeight, this.textArea.scrollHeight) + 16;

        // Set the parent field height, then recompute textarea height.
        this.field.style.height = height + 'px';
        this.textArea.style.height = '100%';
    }
}

