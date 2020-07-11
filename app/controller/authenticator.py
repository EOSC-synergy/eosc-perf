'''This module acts as a fascade between the IOController
and the EGI Check-In authentication system'''

DEFAULT_AUTH_URL = ""

class Authenticator:

    def __init__(self, auth_url=DEFAULT_AUTH_URL):
        self.auth_url = auth_url
        self.token = None
     
    def authenticate_user(self):
        #TODO: implement
        return False

    def is_authenticated(self):
        #TODO: implement
        return False

    def sign_out(self):
        #TODO: implement
        return False

    def is_admin(self):
        #TODO: implement
        return False

    def get_auth_url(self):
        return self.auth_url

    def _set_token(self):
        #TODO: implement
        self.token = None 

    def _val_token(self):
        #TODO: implement
        return False


