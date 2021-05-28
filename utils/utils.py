import re
import base64


class AuthenticationFailedError(Exception):
    def __init__(self, message="Authentication Failed"):
        super().__init__(message)


class NotUpdatableError(Exception):
    def __init__(self, message="not updatable user_id and password"):
        super().__init__(message)


def get_auth(request):
    try:
        auth = request.headers.get("Authorization")
        m = re.match(r"Basic (.*)", auth)
        token = base64.b64decode(m.group(1))
        auth_user_id, auth_password = token.decode().split(":")
        return auth_user_id, auth_password
    except:
        raise AuthenticationFailedError()


def check_updatable(request):
    if request.get_json().get("user_id") or request.get_json().get("password"):
        raise NotUpdatableError()
