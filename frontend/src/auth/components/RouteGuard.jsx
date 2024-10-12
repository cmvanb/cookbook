import { createEffect } from 'solid-js'
import { useNavigate } from '@solidjs/router'

import AuthService from '@/auth/service'

function RouteGuard (props) {
    const navigate = useNavigate()

    createEffect(() => {
        const token = AuthService.getAccessToken()

        if (!token) {
            navigate('/login', { replace: true })
            return
        }
    })

    return (
        <>
            {props.children}
        </>
    )
}

export default RouteGuard
