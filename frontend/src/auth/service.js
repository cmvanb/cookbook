import { request } from '@/core/api/request'

export default class AuthService {
    static async loginAccessToken(data) {
        const { formData } = data

        const response = await request({
            method: 'POST',
            url: '/login/access-token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                400: 'Bad Request',
                422: 'Validation Error',
            },
        })

        if (response.access_token) {
            localStorage.setItem('access_token', response.access_token)
        }
    }

    static async testAccessToken() {
        try {
            await request({
                method: 'POST',
                url: '/login/test-token',
                errors: {
                    401: 'Unauthorized',
                    403: 'Forbidden',
                },
            })
        } catch (error) {
            this.logout()
        }
    }

    static getAccessToken() {
        return localStorage.getItem('access_token')
    }

    static isLoggedIn() {
        return this.getAccessToken() !== null
    }

    static logout() {
        localStorage.removeItem('access_token')
    }
}
