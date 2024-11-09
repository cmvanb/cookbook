import { createForm } from '@felte/solid'
import { reporter } from '@felte/reporter-solid'
import { createEffect, createSignal } from 'solid-js'
import { useNavigate } from '@solidjs/router'

import AuthService from '@/auth/service'
import { ErrorCard, FormField, Page } from '@/core/components'
import { isStringWithValue } from '@/core/utils'
import { validate_all, isValidEmail } from '@/core/validation'
import UsersService from '@/users/service'

function Register() {
    const navigate = useNavigate()

    const [serverError, setServerError] = createSignal({
        message: null,
        renderHelp: null,
        detail: null,
    })

    const handleSubmit = async (data) => {
        await UsersService.register({ body: data })

        navigate('/login')
    }

    const handleError = (error) => {
        switch (error.status) {
            case 400:
                if (error.body.detail === 'Email is already registered') {
                    setServerError({
                        message: 'Email is already registered',
                        renderHelp: () => (
                            <p>Try <a class='link' href={'/login'}>logging in</a>.</p>
                        ),
                    })
                    break
                }
            default:
                setServerError({
                    message: `Server error ${error.status}: ${error.statusText}`,
                    detail: error.body.detail,
                })
                break
        }
    }

    createEffect(async () => {
        await AuthService.testAccessToken()

        if (AuthService.isLoggedIn()) {
            navigate('/recipes')
        }
    })

    const { form, errors } = createForm({
        onSubmit: handleSubmit,
        onError: handleError,
        extend: [reporter],
        validate: (values) => {
            const errors = {}

            errors.email = validate_all(
                values.email,
                [(v) => !isStringWithValue(v),
                    'Email is required'],
                [(v) => v && !isValidEmail(v),
                    'Must be a valid email'],
            )
            errors.password = validate_all(
                values.password,
                [(v) => !isStringWithValue(v),
                    'Password is required'],
                [(v) => v && v.length < 8,
                    'Must be at least 8 characters'],
            )
            errors.confirmpassword = validate_all(
                values.confirmpassword,
                [(v) => !isStringWithValue(v),
                    'Please confirm your password'],
                [(v) => v && values.password && v !== values.password,
                    'Passwords must match'],
            )

            return errors
        },
    })

    return (
        <Page>
            <article>
                <section class='header center-align'>
                    <h4>Register</h4>
                </section>
                <section>
                    <form use:form>
                        {serverError().message !== null && (
                            <ErrorCard
                                message={serverError().message}
                                detail={serverError().detail}
                                renderHelp={serverError().renderHelp}
                            />
                        )}
                        <FormField
                            name='email'
                            type='email'
                            label='Email'
                            autocomplete
                            required
                            errors={errors}
                        />
                        <FormField
                            name='password'
                            type='password'
                            label='Password'
                            required
                            errors={errors}
                        />
                        <FormField
                            name='confirmpassword'
                            type='password'
                            label='Confirm password'
                            required
                            errors={errors}
                        />

                        <nav class='row'>
                            <button type='submit'>Register</button>
                            <a href={'/login'}>
                                <p>Have an account?</p>
                            </a>
                        </nav>
                    </form>
                </section>
            </article>
        </Page>
    )
}

export default Register
