import { createContext, useContext } from 'solid-js';

import { authStore } from './store';

const AuthContext = createContext();

function AuthProvider(props) {
    return (
        <AuthContext.Provider
            value={{
                authStore,
            }}
        >
            {props.children}
        </AuthContext.Provider>
    );
}

function useAuthContext() {
    return useContext(AuthContext);
}

export { AuthProvider, useAuthContext };
