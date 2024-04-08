from decouple import config


class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://"
        + config("DB_USER")
        + ":"
        + config("DB_PASSWORD")
        + "@"
        + config("DB_HOST")
        + "/"
        + config("DB_NAME")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = config("TRACK_MODIFICATIONS")


class DevelopmentConfig(Config):
    DEBUG = True


config = {"development": DevelopmentConfig}
