import { createForm } from '@felte/solid'
import { reporter } from '@felte/reporter-solid'
import { createEffect, createSignal } from 'solid-js'
import { useNavigate } from '@solidjs/router'

import AuthService from '@/auth/service'
import { FormField, Page } from '@/core/components'
import { isStringWithValue } from '@/core/utils'

function Login() {
    const navigate = useNavigate()

    const [loginError, setLoginError] = createSignal({ error_message: '', help_message: null })

    const handleSubmit = async (data) => {
        await AuthService.loginAccessToken({ formData: data })

        if (AuthService.isLoggedIn()) {
            setLoginError({ error_message: '', help_message: null })
            navigate('/recipes')
        }
    }

    const handleLoginError = (error) => {
        switch (error.status) {
            case 400:
                if (error.body.detail === 'Incorrect email or password') {
                    setLoginError({
                        error_message: 'Incorrect email or password',
                        /* TODO: Password reset link */
                        help_message: () => (
                            <p>Try entering your information again.</p>
                        ),
                    })
                    break
                }
                if (error.body.detail === 'Inactive user') {
                    setLoginError({
                        error_message: 'Your account is inactive',
                        help_message: () => (
                            <p>Please contact your system administrator.</p>
                        ),
                    })
                    break
                }
            default:
                setLoginError({
                    error_message: `Server error ${error.status}: ${error.statusText}`,
                    help_message: () => (
                        <p>Detail: {error.body.detail}</p>
                    ),
                })
                break
        }
    }

    createEffect(async () => {
        await AuthService.testAccessToken()

        if (AuthService.isLoggedIn()) {
            setLoginError({ error_message: '', help_message: null })
            navigate('/recipes')
        }
    })

    const { form, errors } = createForm({
        onSubmit: handleSubmit,
        onError: handleLoginError,
        extend: [reporter],
    })

    return (
        <Page>
            <article>
                <section class='header center-align'>
                    <h4>Log In</h4>
                </section>
                <section>
                    <form use:form>
                        {isStringWithValue(loginError().error_message) && (
                            <>
                                <article class='border error-container'>
                                    <h6>{loginError().error_message}</h6>
                                    {loginError().help_message()}
                                </article>
                                <br/>
                            </>
                        )}
                        <FormField
                            name='username'
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

                        <nav class='row'>
                            <button type='submit' value='Log In'>Log In</button>
                            <a href={'/register'}>
                                <p>Need an account?</p>
                            </a>
                        </nav>
                    </form>
                </section>
            </article>
        </Page>
    )
}

export default Login
