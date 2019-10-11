from .models import Token
from jose import jwt
from django.contrib.auth import get_user_model

User = get_user_model()


class TokenBackend(object):
    def authenticate(self, token=None):
        """
        Try to find a user with the given token
        """
        try:
            t = Token.objects.get(key=token)
            return t.user
        except Token.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class JWTAuthentication(object):

    """
    Simple token based authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:
    Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        try:
            token = auth[1].decode("utf-8")
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, payload):

        decoded_dict = jws.verify(payload, 'seKre8', algorithms=['HS256'])

        username = decoded_dict.get('username', None)
        expiry = decoded_dict.get('expiry', None)

        try:
            usr = User.objects.get(username=username)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not usr.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        if expiry < datetime.date.today():
            raise exceptions.AuthenticationFailed(_('Token Expired.'))

        return (usr, payload)

    def authenticate_header(self, request):
        return 'Token'
