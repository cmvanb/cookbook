import { request } from '@/core/api/request'

export default class UsersService {
    static async register(data) {
       const { body } = data

        const response = await request({
            method: 'POST',
            url: '/users/register',
            body: body,
            mediaType: 'application/json',
            errors: {
                422: 'Validation Error',
            },
        })

        return response
    }
}
