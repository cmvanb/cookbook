#-------------------------------------------------------------------------------
# Module entry point
#-------------------------------------------------------------------------------

from cookbook.application import create_app

# WSGI will hook onto this variable.
app = create_app()

# This is the entry point for the development server. Don't run on prod.
if __name__ == '__main__':
    app.run()
