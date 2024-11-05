import { createForm } from '@felte/solid'
import { reporter } from '@felte/reporter-solid'
import { createSignal } from 'solid-js'
import { useNavigate } from '@solidjs/router'

import UsersService from '@/users/service'
import FormField from '@/core/components/FormField'
import Page from '@/core/pages/Page'
import { isStringWithValue } from '@/core/utils'

function Register() {
    const navigate = useNavigate()

    const [registerError, setRegisterError] = createSignal({ error_message: '', help_message: null })

    const handleSubmit = async (data) => {
        await UsersService.register({ body: data })

        setRegisterError({ error_message: '', help_message: null })
        navigate('/login',)
    }

    const handleRegisterError = (error) => {
        switch (error.status) {
            case 400:
                if (error.body.detail === 'Email is already registered') {
                    setRegisterError({
                        error_message: 'Email is already registered',
                        help_message: () => (
                            <p>Try <a class='link' href={'/login'}>logging in</a>.</p>
                        ),
                    })
                    break
                }
            default:
                setRegisterError({
                    error_message: `Server error ${error.status}: ${error.statusText}`,
                    help_message: () => (
                        <p>Detail: {error.body.detail}</p>
                    ),
                })
                break
        }
    }

    const { form, errors } = createForm({
        onSubmit: handleSubmit,
        onError: handleRegisterError,
        extend: [reporter],
        validate: (values) => {
            const errors = {}

            if (!values.email
                || !/^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+/.test(values.email)) {
                errors.email = 'Must be a valid email'
            }

            if (!values.password) {
                errors.password = 'Must not be empty'
            }

            if (values.password
                && values.password.length < 8) {
                errors.password = 'Must be at least 8 characters'
            }

            if (!values.confirmpassword) {
                errors.confirmpassword = 'Please confirm your password'
            }

            if (values.password
                && values.confirmpassword
                && values.password !== values.confirmpassword) {
                errors.confirmpassword = 'Passwords must match'
            }

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
                        {isStringWithValue(registerError().error_message) && (
                            <>
                                <article class='border error-container'>
                                    <h6>{registerError().error_message}</h6>
                                    {registerError().help_message()}
                                </article>
                                <br/>
                            </>
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
