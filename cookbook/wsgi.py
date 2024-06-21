from cookbook.application import create_app

app = create_app()

# NOTE: The WSGI server will start the application callable. The following entry
# point is only for development.
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
