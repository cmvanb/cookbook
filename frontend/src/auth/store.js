import { createStore } from 'solid-js/store';

const initialState = {
    token: null,
};

const [ authStore, setAuthStore ] = createStore(initialState);

export { authStore, setAuthStore };
