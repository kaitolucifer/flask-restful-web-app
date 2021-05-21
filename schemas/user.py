import re

from marshmallow import pre_load

from ma import ma
from models.user import UserModel


class NonASCIIError(Exception):
    def __init__(self, message):
        super().__init__(message)


class LengthTooShortError(Exception):
    def __init__(self, message):
        super().__init__(message)


class LengthTooLongError(Exception):
    def __init__(self, message):
        super().__init__(message)


class RequiredError(Exception):
    def __init__(self, message="required user_id and password"):
        super().__init__(message)


class GetUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True

    @pre_load
    def _pre_load(self, data, **kwargs):
        if not data.get('user_id') or not data.get("password"):
            raise RequiredError()
        return data


class PatchUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True

    @pre_load
    def _pre_load(self, data, **kwargs):
        if not data.get('user_id') or not data.get("password"):
            raise RequiredError()

        if not data.get("nickname") and not data.get("comment"):
            raise RequiredError(message="required nickname or comment")

        return data


class CloseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True

    @pre_load
    def _pre_load(self, data, **kwargs):
        if not data.get('user_id') or not data.get("password"):
            raise RequiredError()
        return data


class SignupSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True

    @pre_load
    def _pre_load(self, data, **kwargs):
        if data.get('password'):
            data['password'] = re.sub(r'\s', '', data['password'])

            if len(data['password']) < 6:
                raise LengthTooShortError("invalid password: too short")
            elif len(data['password']) > 20:
                raise LengthTooLongError("invalid password: too long")

            try:
                data['password'].encode('ascii')
            except UnicodeEncodeError:
                raise NonASCIIError("invalid password: Non-ASCII character")
        else:
            raise RequiredError()

        if data.get('user_id'):
            data['user_id'] = re.sub(r'\s', '', data['user_id'])

            if len(data['user_id']) < 6:
                raise LengthTooShortError("invalid user_id: too short")
            elif len(data['user_id']) > 20:
                raise LengthTooLongError("invalid user_id: too long")

            try:
                data['user_id'].encode('ascii')
            except UnicodeEncodeError:
                raise NonASCIIError("invalid user_id: Non-ASCII character")
        else:
            raise RequiredError()

        return data
