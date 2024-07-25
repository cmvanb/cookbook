#-------------------------------------------------------------------------------
# Main Views
#-------------------------------------------------------------------------------

from flask import Blueprint, redirect, url_for


blueprint = Blueprint(
    'main', __name__,
    url_prefix='/',
    static_folder='static',
    template_folder='templates',
)


@blueprint.route('/')
def index():
    """ Index view. Redirects to the login page. """

    # TODO: Render a nice splash page instead of redirecting.
    return redirect(url_for('auth.login'))
