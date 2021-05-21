from db import db


class SameUserIDError(Exception):
    def __init__(self, message="already same user_id is used"):
        super().__init__(message)


class UserNotExistError(Exception):
    def __init__(self, message="No user found"):
        super().__init__(message)


class InvalidPasswordError(Exception):
    def __init__(self, message="invalid password"):
        super().__init__(message)


class NoPermissionError(Exception):
    def __init__(self, message="No Permission for Update"):
        super().__init__(message)


class UserModel(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.String(64), nullable=False, primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    nickname = db.Column(db.String(64))
    comment = db.Column(db.String(128))

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def save_to_db(self):
        if self.find_by_user_id(self.user_id):
            raise SameUserIDError()
        db.session.add(self)
        db.session.commit()

    def update_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
        # deleteの冪乗性を維持
        except:
            pass

    def authenticate(self):
        user = self.find_by_user_id(self.user_id)
        if not user:
            raise UserNotExistError()
        elif self.password != user.password:
            raise InvalidPasswordError()

    def check_permission(self, user_id):
        if self.user_id != user_id:
            raise NoPermissionError()
