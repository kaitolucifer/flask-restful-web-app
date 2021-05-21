import re
import base64


class AuthenticationFaildError(Exception):
    def __init__(self, message="Authentication Faild"):
        super().__init__(message)


class NotUpdatableError(Exception):
    def __init__(self, message="not updatable user_id and password"):
        super().__init__(message)


def get_auth(request):
    try:
        auth = request.headers.get("Authorization")
        m = re.match(r"Basic (.*)", auth)
        token = base64.b64decode(m.group(1))
        auth_user_id, auth_password = token.split(":")
        return auth_user_id, auth_password
    except:
        raise AuthenticationFaildError()


def check_updatable(request):
    if request.get_json().get("user_id") or request.get_json().get("password"):
        raise Exception(NotUpdatableError)
