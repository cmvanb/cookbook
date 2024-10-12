export const isString = (value) => typeof value === 'string'

export const isStringWithValue = (value) => isString(value) && value.length > 0
