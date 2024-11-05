import { createEffect } from 'solid-js'
import { useNavigate } from '@solidjs/router'

import AuthService from '@/auth/service'

function RouteGuard (props) {
    const navigate = useNavigate()

    createEffect(() => {
        if (!AuthService.isLoggedIn()) {
            navigate('/login', { repace: true })
        }
    })

    return (
        <>
            {props.children}
        </>
    )
}

export default RouteGuard
