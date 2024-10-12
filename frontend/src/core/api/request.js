import axios from 'axios'

import { ApiError } from '@/core/api/error.js'
import { isString, isStringWithValue } from '@/core/utils.js'

const config = {
    baseURL: 'http://localhost:8000/api',
}

const isBlob = (value) => value instanceof Blob

const isFormData = (value) => value instanceof FormData

const isSuccess = (status) => status >= 200 && status < 300

const getQueryString = (params) => {
    const qs = []

    const append = (key, value) => {
        qs.push(`${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
    }

    const encodePair = (key, value) => {
        if (value === undefined || value === null) {
            return
        }

        if (Array.isArray(value)) {
            value.forEach((v) => append(key, v))

        } else if (typeof value === 'object') {
            Object.keys(value).forEach((subKey) => {
                encodePair(`${key}[${subKey}]`, value[subKey])
            })
            Object.entries(value).forEach(([k, v]) => encodePair(`${key}[${k}]`, v))

        } else {
            append(key, value)
        }
    }

    Object.entries(params).forEach(([key, value]) => encodePair(key, value))

    return qs.length ? `?${qs.join('&')}` : ''
}

const getURL = (options) => {
    // Insert path parameters.
    const path = options.url
        .replace(/{(.*?)}/g, (substring, group) => {
            if (options.path.hasOwnProperty(group)) {
                return encodeURI(String(options.path[group]))
            }
            return substring
        })

    const url = config.baseURL + path

    return options.query ? url + getQueryString(options.query) : url
}

const getFormData = (options) => {
    if (options.formData) {
        const formData = new FormData()

        const process = (key, value) => {
            if (isString(value) || isBlob(value)) {
                formData.append(key, value)
            } else {
                formData.append(key, JSON.stringify(value))
            }
        }

        Object.entries(options.formData)
            .filter(([, value]) => value !== undefined && value !== null)
            .forEach(([key, value]) => {
                if (Array.isArray(value)) {
                    value.forEach((v) => process(key, v))
                } else {
                    process(key, value)
                }
            })

        return formData
    }

    return undefined
}

const getAccessToken = () => {
    return localStorage.getItem('access_token')
}

const getHeaders = (options) => {
    const token = getAccessToken()

    const headers =
        Object.entries({
            Accept: 'application/json',
            ...options.headers,
        })
        .filter(([, value]) => value !== undefined && value !== null)
        .reduce((headers, [key, value]) => ({
            ...headers,
            [key]: String(value),
        }), {})

    if (token !== null
        && isStringWithValue(token)) {
        headers['Authorization'] = `Bearer ${token}`
    }

    if (options.body !== undefined) {
        if (options.mediaType) {
            headers['Content-Type'] = options.mediaType

        } else if (isBlob(options.body)) {
            headers['Content-Type'] = options.body.type || 'application/octet-stream'

        } else if (isString(options.body)) {
            headers['Content-Type'] = 'text/plain'

        } else if (!isFormData(options.body)) {
            headers['Content-Type'] = 'application/json'
        }
    } else if (options.formData !== undefined) {
        if (options.mediaType) {
            headers['Content-Type'] = options.mediaType
        }
    }

    return headers
}

const getRequestBody = (options) => {
    if (options.body) {
        return options.body
    }

    return undefined
}

const sendRequest = async ({
    options,
    url,
    body,
    formData,
    headers,
}) => {
    let requestConfig = {
        data: body ?? formData,
        headers,
        method: options.method,
        url,
    }

    try {
        return await axios.request(requestConfig)

    } catch (error) {
        if (error.response) {
            return error.response
        }

        throw error
    }
}

const getResponseHeader = (response, header) => {
    if (header) {
        const content = response.headers[header]

        if (isString(content)) {
            return content
        }
    }

    return undefined
}

const getResponseBody = (response) => {
    if (response.status !== 204) {
        return response.data
    }

    return undefined
}

const catchErrorCodes = (
    options,
    result,
) => {
    const errors = {
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Payload Too Large',
        414: 'URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Range Not Satisfiable',
        417: 'Expectation Failed',
        418: 'Im a teapot',
        421: 'Misdirected Request',
        422: 'Unprocessable Content',
        423: 'Locked',
        424: 'Failed Dependency',
        425: 'Too Early',
        426: 'Upgrade Required',
        428: 'Precondition Required',
        429: 'Too Many Requests',
        431: 'Request Header Fields Too Large',
        451: 'Unavailable For Legal Reasons',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        506: 'Variant Also Negotiates',
        507: 'Insufficient Storage',
        508: 'Loop Detected',
        510: 'Not Extended',
        511: 'Network Authentication Required',
        ...options.errors,
    }

    const error = errors[result.status]
    if (error) {
        throw new ApiError(options, result, error)
    }

    if (!result.ok) {
        const errorStatus = result.status ?? 'unknown'
        const errorStatusText = result.statusText ?? 'unknown'
        const errorBody = (() => {
            try {
                return JSON.stringify(result.body, null, 2)
            } catch (e) {
                return undefined
            }
        })()

        throw new ApiError(
            options,
            result,
            `Generic Error: status: ${errorStatus} status text: ${errorStatusText} body: ${errorBody}`
        )
    }
}

export const request = (options) => {
    // TODO: Consider using a cancelable promise.
    return new Promise(async (resolve, reject) => {
        try {
            const url = getURL(options)
            const formData = getFormData(options)
            const headers = getHeaders(options)
            const body = getRequestBody(options)

            let response = await sendRequest({
                options: options,
                url: url,
                body: body,
                formData: formData,
                headers: headers,
            })

            const responseBody = await getResponseBody(response)
            const responseHeader = getResponseHeader(response, options.responseHeader)

            const result = {
                url,
                ok: isSuccess(response.status),
                status: response.status,
                statusText: response.statusText,
                body: responseHeader ?? responseBody,
            }

            catchErrorCodes(options, result)

            resolve(result.body)
        } catch (error) {
            reject(error)
        }
    })
}
