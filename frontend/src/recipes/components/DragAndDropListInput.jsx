import { createSignal, For } from 'solid-js'
import { dndzone } from 'solid-dnd-directive';

import '@/recipes/components/DragAndDropListInput.css'


function DragAndDropListInput({ type, label, items, setItems }) {
    const buttonLabel = `Add ${label.slice(0, -1).toLowerCase()}`

    const [count, setCount] = createSignal(items().length)

    const handleDndEvent = (e) => {
        const { items: newItems } = e.detail

        setItems(newItems)
    }

    const addItem = () => {
        const index = count()
        setItems([...items(), { id: index, text: '' }])
        setCount(count() + 1)
    }

    const editItem = (index, text) => {
        items()[index].text = text
    }

    const deleteItem = (index) => {
        setItems(items().filter((_, i) => i !== index))
    }

    return (
        <div class='dnd-field'>
            <label class='dnd-label'>{label}</label>
            <div
                class='dnd-border'
                use:dndzone={{
                    items,
                    type,
                    dropTargetStyle: {
                        outline: 'var(--primary) solid 1px',
                    },
                }}
                on:consider={handleDndEvent}
                on:finalize={handleDndEvent}
            >
                <For each={items()}>{(item, index) => {
                    return (
                        <div class='dnd-item small-elevate'>
                            <div class='row'>
                                <i class='secondary-text'>drag_indicator</i>
                                <input
                                    class='dnd-item-input'
                                    type='text'
                                    value={item.text}
                                    onChange={(e) => editItem(index(), e.target.value)}
                                />
                                <button
                                    class='primary-text transparent small circle'
                                    type='button'
                                    onClick={() => deleteItem(index())}
                                >
                                    <i>delete</i>
                                </button>
                            </div>
                        </div>
                    )
                }}</For>
            </div>
            <button
                class='dnd-add-button small fill'
                type='button'
                onClick={addItem}
            >
                <i>Add</i>
                <span>{buttonLabel}</span>
            </button>
        </div>
    )
}

export default DragAndDropListInput
