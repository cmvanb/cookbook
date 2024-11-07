import { Show, createSignal, createRenderEffect, on } from 'solid-js'
import { useLocation, useNavigate } from '@solidjs/router'

import AuthService from '@/auth/service'

function RouteGuard (props) {
    const location = useLocation()
    const navigate = useNavigate()

    const [authenticated, setAuthenticated] = createSignal(false)

    const checkAuth = async () => {
        setAuthenticated(false)

        await AuthService.testAccessToken()

        if (AuthService.isLoggedIn()) {
            setAuthenticated(true)
        } else {
            navigate('/login', { replace: true })
        }
    }

    createRenderEffect(on(() => location.pathname, checkAuth))

    return (
        <>
            <Show when={authenticated()}>
                {props.children}
            </Show>
        </>
    )
}

export default RouteGuard
