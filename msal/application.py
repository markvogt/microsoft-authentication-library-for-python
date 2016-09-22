from . import request


class ClientApplication(object):
    DEFAULT_AUTHORITY = "https://login.microsoftonline.com/common/"

    def __init__(
            self, client_id,
            validate_authority=True, authority=DEFAULT_AUTHORITY):
        self.client_id = client_id
        self.validate_authority = validate_authority
        self.authority = authority
#    def aquire_token_silent(
#            self, scopes, user=None, authority=None, policy=None,
#            force_refresh=False):
#        pass


class PublicClientApplication(ClientApplication):
    DEFAULT_REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

    def __init__(self, client_id, redirect_uri=DEFAULT_REDIRECT_URI, **kwargs):
        super(PublicClientApplication, self).__init__(client_id, **kwargs)
        self.redirect_uri = redirect_uri

class ConfidentialClientApplication(ClientApplication):
    def __init__(self, client_id, client_credential, user_token_cache, **kwargs):
        """
        :param client_credential: It can be a string containing client secret,
            or an X509 certificate object.
        """
        super(ConfidentialClientApplication, self).__init__(client_id, **kwargs)
        self.client_credential = client_credential
        self.user_token_cache = user_token_cache
        self.app_token_cache = None  # TODO

    def acquire_token_for_client(self, scope, policy=''):
        return request.ClientCredentialRequest(
            client_id=self.client_id, client_credential=self.client_credential,
            scope=scope, policy=policy, authority=self.authority).run()
