"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flaat import Flaat
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
cache = Cache()
migrate = Migrate()
api = Api()
db = SQLAlchemy()


class MyFlaat(Flaat):
    """Monkeypatch flaat to solve lazy configuration
    https://github.com/indigo-dc/flaat/issues/32

    For more information see: 
    https://flask.palletsprojects.com/en/2.0.x/extensiondev/#the-extension-code
    """

    def __init__(self, app=None):
        self.app = app
        self.admin_assurance = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        super().__init__()

        self.set_web_framework('flask')
        self.set_cache_lifetime(120)  # seconds; default is 300
        self.set_trusted_OP_list([
            'https://aai-dev.egi.eu/oidc'
        ])

        # flaat.set_trusted_OP_file('/etc/oidc-agent/issuer.config')
        # flaat.set_OP_hint("helmholtz")
        # flaat.set_OP_hint("google")
        self.set_timeout(3)

        # verbosity:
        #     0: No output
        #     1: Errors
        #     2: More info, including token info
        #     3: Max
        self.set_verbosity(0)
        # flaat.set_verify_tls(True)

        # Required for using token introspection endpoint:
        client_id = app.config['EGI_CLIENT_ID']
        self.set_client_id(client_id)

        client_secret = app.config['EGI_CLIENT_SECRET']
        self.set_client_secret(client_secret)

        admin_assurance = app.config['ADMIN_ASSURANCE']
        self.admin_assurance = admin_assurance


flaat = MyFlaat()
