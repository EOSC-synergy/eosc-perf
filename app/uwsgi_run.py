from . import create_app

# TODO: a way to launch the uwsgi app with debug on or off?
app = create_app(True)
