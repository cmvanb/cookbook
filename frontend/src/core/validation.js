export const constants = {
    STRING_MAX: 255,
    TEXT_MAX: 4000,
    NUMBER_MAX: 999999999,
}

export const validate = (value, rule) => {
    const [condition, error] = rule
    if (condition(value)) {
        return error
    }
    return null
}

export const validate_all = (value, ...rules) => {
    const errors = []
    for (const rule of rules) {
        const e = validate(value, rule)
        e && errors.push(e)
    }
    return errors
}

export const isValidEmail = (value) => {
    return /^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+/.test(value)
}
