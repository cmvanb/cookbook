#-------------------------------------------------------------------------------
# Authentication Utilities
#-------------------------------------------------------------------------------

import functools

from flask import g, redirect, url_for


def login_required(view):
    """ Decorator to require authentication for a view. """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
