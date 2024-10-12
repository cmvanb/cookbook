import { ValidationMessage } from '@felte/reporter-solid'

function FormField ({ name, type, label, errors, ...props }) {
    const baseClasses = ['field', 'label', 'border']

    const classes = () =>
        errors()[name] && baseClasses.concat('invalid')
            || baseClasses

    return (
        <div class={classes().join(' ')}>
            <input
                id={name}
                type={type}
                name={name}
                {...props}
            />
            <label for={name}>{label}</label>
            <ValidationMessage for={name}>
                {(messages) => <span class='error'>{messages?.[0]}</span>}
            </ValidationMessage>
        </div>
    )
}

export default FormField
