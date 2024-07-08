#-------------------------------------------------------------------------------
# Module entry point
#-------------------------------------------------------------------------------

from cookbook.application import create_app

# WSGI will hook onto this variable.
app = create_app()
