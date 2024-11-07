import { request } from '@/core/api/request'

export default class RecipeService {

    static async createRecipe(data) {
        const { body } = data

        const response = await request({
            method: 'POST',
            url: '/recipes/create',
            body: body,
            mediaType: 'application/json',
            errors: {
                401: 'Unauthorized',
                403: 'Forbidden',
                422: 'Validation Error',
            },
        })

        return response
    }

    static async getRecipes() {
        const response = await request({
            method: 'GET',
            url: `/recipes/read/`,
            errors: {
                401: 'Unauthorized',
                403: 'Forbidden',
            },
        })

        return response
    }

    static async getRecipe(id) {
        const response = await request({
            method: 'GET',
            url: `/recipes/read/${id}`,
            errors: {
                401: 'Unauthorized',
                403: 'Forbidden',
            },
        })

        return response
    }

    static async getPublicRecipes() {
        const response = await request({
            method: 'GET',
            url: `/recipes/read/public/`,
            errors: {
                401: 'Unauthorized',
                403: 'Forbidden',
            },
        })

        return response
    }

    static async getPublicRecipe(id) {
        const response = await request({
            method: 'GET',
            url: `/recipes/read/public/${id}`,
            errors: {
                401: 'Unauthorized',
                403: 'Forbidden',
            },
        })

        return response
    }

    static async updateRecipe(id, data) {
        const { body } = data

        const response = await request({
            method: 'PUT',
            url: `/recipes/update/${id}`,
            body: body,
            mediaType: 'application/json',
            errors: {
                401: 'Unauthorized',
                403: 'Forbidden',
                422: 'Validation Error',
            },
        })

        return response
    }

    static async deleteRecipe(id) {
        await request({
            method: 'DELETE',
            url: `/recipes/delete/${id}`,
            errors: {
                401: 'Unauthorized',
                403: 'Forbidden',
            },
        })
    }
}
