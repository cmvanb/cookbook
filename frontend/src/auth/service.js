import { request } from './request'

export class AuthService {
    static loginAccessToken(data) {
        const { formData } = data;

        return request({
            method: 'POST',
            url: '/api/login/access-token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: 'Validation Error',
            },
        });
    }
}
