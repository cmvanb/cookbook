export const isString = (value) => typeof value === 'string'

export const isStringWithValue = (value) => isString(value) && value.length > 0

export const isNumber = (value) => typeof value === 'number'

export const isNumberWithValue = (value) => isNumber(value) && value !== NaN
