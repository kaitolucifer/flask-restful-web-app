from flask import request
from flask_restful import Resource

from schemas.user import CloseSchema, SignupSchema, PatchUserSchema, NonASCIIError, LengthTooLongError, LengthTooShortError, RequiredError
from models.user import UserModel, SameUserIDError, InvalidPasswordError, UserNotExistError, NoPermissionError
from utils.utils import get_auth, AuthenticationFaildError, check_updatable, NotUpdatableError
from db import db

patch_user_schema = PatchUserSchema()
close_schema = CloseSchema()
signup_schema = SignupSchema()


class User(Resource):
    @classmethod
    def get(cls, user_id):
        try:
            auth_user_id, auth_password = get_auth(request)
            data = {"user_id": auth_user_id,
                    "password": auth_password}
        except AuthenticationFaildError as err:
            return {"message": str(err)}, 401
        except UserNotExistError as err:
            return {"message": str(err)}, 404

        user = UserModel.find_by_user_id(user_id)
        if not user:
            return {"message": "No User found"}, 404

        user_data = {"user_id": user.user_id}
        if user.comment != None:
            user_data["comment"] = user.comment

        if user.nickname != None:
            user_data["nickname"] = user.nickname
        else:
            user_data["nickname"] = user_id

        return {"message": "User details by user_id",
                "user": user_data}, 200

    @classmethod
    def patch(cls, user_id):
        try:
            auth_user_id, auth_password = get_auth(request)
            check_updatable(request)
            data = {"user_id": auth_user_id,
                    "password": auth_password,
                    "nickname": request.get_json().get("nickname"),
                    "comment": request.get_json().get("comment")}
            user = patch_user_schema.load(data)
            user.authenticate()
            user.check_permission(user_id)
            user.delete_from_db()
            user.save_to_db()
            return {
                "message": "User successfully updated",
                "recipe": [
                    {
                        "nickname": data["nickname"],
                        "comment": data["comment"],
                    }
                ]
            }, 200
        except AuthenticationFaildError as err:
            return {"message": str(err)}, 401
        except NotUpdatableError as err:
            return {
                "message": "User updation Faild",
                "cause": str(err)
            }, 400
        except InvalidPasswordError:
            return {"message": "Authentication Faild"}, 401
        except UserNotExistError as err:
            return {"message": str(err)}, 404
        except NoPermissionError as err:
            return {"message": str(err)}, 403
        except RequiredError as err:
            return {"message": str(err)}, 400


class Signup(Resource):
    @classmethod
    def post(cls):
        try:
            data = request.get_json()
            user = signup_schema.load(data)
            user.save_to_db()
            return {
                "message": "Account successfully created",
                "user": {
                    "user_id": user.user_id,
                    "nickname": user.nickname
                }
            }
        except RequiredError as err:
            return {
                "message": "Account creation failed",
                "cause": str(err)
            }, 400
        except NonASCIIError as err:
            return {
                "message": "Account creation failed",
                "cause": str(err)
            }, 400
        except LengthTooShortError as err:
            return {
                "message": "Account creation failed",
                "cause": str(err)
            }, 400
        except LengthTooLongError as err:
            return {
                "message": "Account creation failed",
                "cause": str(err)
            }, 400
        except SameUserIDError as err:
            return {
                "message": "Account creation failed",
                "cause": str(err)
            }, 400


class Close(Resource):
    @classmethod
    def post(cls):
        try:
            auth_user_id, auth_password = get_auth(request)
            data = {"user_id": auth_user_id, "password": auth_password}
            user = close_schema.load(data)
            user.authenticate()
            user.delete_from_db()
        except AuthenticationFaildError as err:
            return {"message": str(err)}, 401
        except InvalidPasswordError:
            return {"message": "Authentication Faild"}, 401
        except (UserNotExistError, RequiredError):
            pass
        return {"message": "Account and user successfully removed"}
