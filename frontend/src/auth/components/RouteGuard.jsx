import { createEffect } from 'solid-js';
import { useNavigate } from '@solidjs/router';

function RouteGuard (props) {
    const navigate = useNavigate();
    const token = sessionStorage.getItem('token');

    createEffect(() => {
        if (!token) {
            navigate('/login', { replace: true });
        }
    })

    return (
        <>
            {props.children}
        </>
    )
}

export default RouteGuard;
