/*------------------------------------------------------------------------------
    Entry point for the frontend application.
------------------------------------------------------------------------------*/
/* @refresh reload */

import { render } from 'solid-js/web'

// Local styles will override global styles.
import 'beercss'
import './index.css'

import App from './App'

const root = document.getElementById('root')

if (import.meta.env.DEV && !(root instanceof HTMLElement)) {
    throw new Error(
        'Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?',
    )
}

render(() => (<App />), root)
