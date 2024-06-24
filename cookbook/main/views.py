#-------------------------------------------------------------------------------
# Main Views
#-------------------------------------------------------------------------------

from flask import Blueprint, redirect, url_for

# Main Blueprint
#-------------------------------------------------------------------------------
blueprint = Blueprint(
    'main', __name__,
    url_prefix='/',
    static_folder='static',
    template_folder='templates',
)

# Index view.
#-------------------------------------------------------------------------------
@blueprint.route('/')
def index():
    # TODO: Render a nice splash page instead of redirecting.
    return redirect(url_for('auth.login'))
