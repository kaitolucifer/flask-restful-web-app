from sqlalchemy.pool import SingletonThreadPool

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        ...

    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self):
        return {"poolclass": SingletonThreadPool}


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return "sqlite:///user.db"
