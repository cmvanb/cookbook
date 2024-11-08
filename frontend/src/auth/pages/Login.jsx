import { createForm } from '@felte/solid'
import { reporter } from '@felte/reporter-solid'
import { createEffect, createSignal } from 'solid-js'
import { useNavigate } from '@solidjs/router'

import AuthService from '@/auth/service'
import { ErrorCard, FormField, Page } from '@/core/components'

function Login() {
    const navigate = useNavigate()

    const [validationError, setValidationError] = createSignal({
        message: null,
        renderHelp: null,
        details: null,
    })

    const handleSubmit = async (data) => {
        await AuthService.loginAccessToken({ formData: data })

        if (AuthService.isLoggedIn()) {
            navigate('/recipes')
        }
    }

    const handleError = (error) => {
        switch (error.status) {
            case 400:
                if (error.body.detail === 'Incorrect email or password') {
                    setValidationError({
                        message: 'Incorrect email or password',
                        /* TODO: Password reset link */
                        renderHelp: () => (
                            <p>Try entering your information again.</p>
                        ),
                    })
                    break
                }
                if (error.body.detail === 'Inactive user') {
                    setValidationError({
                        message: 'Your account is inactive',
                        renderHelp: () => (
                            <p>Please contact your system administrator.</p>
                        ),
                    })
                    break
                }
            default:
                setValidationError({
                    message: `Server error ${error.status}: ${error.statusText}`,
                    details: error.body.detail,
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
    })

    return (
        <Page>
            <article>
                <section class='header center-align'>
                    <h4>Log In</h4>
                </section>
                <section>
                    <form use:form>
                        {validationError().message !== null && (
                            <ErrorCard
                                message={validationError().message}
                                details={validationError().details}
                                renderHelp={validationError().renderHelp}
                            />
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
                            <button type='submit' value='Log In'>
                                Log In
                            </button>
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
